"""Gemini와 Kakao Local API를 활용한 국내 여행 추천 프로그램."""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError


class TravelRecommendation(BaseModel):
    """Gemini가 생성할 여행지 추천 JSON 구조."""

    recommended_city: str = Field(
        description="대한민국 국내 여행지의 시·군·구 또는 지역명"
    )
    weather: str = Field(
        description="입력한 여행 시기의 일반적인 예상 날씨와 옷차림"
    )
    events: list[str] = Field(
        description="행사 또는 축제 후보 목록"
    )
    reason: str = Field(
        description="해당 지역을 추천하는 이유"
    )


class Restaurant(BaseModel):
    """Kakao Local API에서 사용할 음식점 정보."""

    name: str
    category: str
    phone: str
    address: str
    road_address: str
    place_url: str


def validate_date(date_text: str) -> str:
    """YYYY-MM-DD 형식의 날짜인지 확인한다."""

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "날짜는 YYYY-MM-DD 형식으로 입력하세요. 예: 2026-10-15"
        ) from error


def load_api_key(variable_name: str) -> str:
    """환경변수에서 API 키를 안전하게 불러온다."""

    load_dotenv(override=True)
    api_key = os.getenv(variable_name)

    if not api_key:
        raise RuntimeError(
            f"{variable_name}가 설정되지 않았습니다. .env 파일을 확인하세요."
        )

    return api_key


def create_gemini_client() -> genai.Client:
    """Gemini API 클라이언트를 만든다."""

    gemini_api_key = load_api_key("GEMINI_API_KEY")
    return genai.Client(api_key=gemini_api_key)


def recommend_destination(
    client: genai.Client,
    travel_date: str,
) -> TravelRecommendation:
    """Gemini로 여행지를 추천받고 JSON 구조를 검사한다."""

    prompt = f"""
당신은 대한민국 국내 여행 전문 가이드입니다.

여행 날짜는 {travel_date}입니다.
계절, 이동 편의성, 대표 볼거리와 먹거리를 고려하여
대한민국 국내 여행지 한 곳을 추천하세요.

다음 기준을 지켜 주세요.
1. 추천 지역은 대한민국 안에 있어야 합니다.
2. Kakao Local API에서 검색할 수 있도록 대표 도시명으로 작성하세요.
3. 날씨는 확정 예보가 아닌 계절상 일반적인 예상이라고 설명하세요.
4. 행사와 축제는 실제 개최 여부를 별도로 확인해야 하는 후보입니다.
5. 행사 정보마다 반드시 '확인 필요'라는 문구를 넣으세요.
6. 추천 이유는 초보 여행자도 이해하기 쉽게 작성하세요.
"""

    last_error: Exception | None = None

    # 최초 요청이 실패하면 한 번만 더 요청합니다.
    for attempt in range(1, 3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=TravelRecommendation,
                    temperature=0.3,
                ),
            )

            if not response.text:
                raise ValueError("Gemini 응답 내용이 비어 있습니다.")

            return TravelRecommendation.model_validate_json(
                response.text
            )

        except (ValidationError, ValueError) as error:
            last_error = error

            if attempt == 1:
                print("JSON 검증에 실패하여 한 번 더 요청합니다.")

    raise RuntimeError(
        f"Gemini JSON 생성에 실패했습니다: {last_error}"
    )


def search_restaurants(city: str) -> list[Restaurant]:
    """추천 도시의 음식점 5곳을 Kakao Local API로 검색한다."""

    kakao_api_key = load_api_key("KAKAO_REST_API_KEY")

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {kakao_api_key}"
    }

    params = {
        "query": f"{city} 맛집",
        "category_group_code": "FD6",
        "size": 5,
        "sort": "accuracy",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(
            f"Kakao Local API 요청에 실패했습니다: {error}"
        ) from error

    response_data = response.json()
    documents = response_data.get("documents", [])

    restaurants: list[Restaurant] = []

    for document in documents:
        restaurant = Restaurant(
            name=document.get("place_name", "이름 없음"),
            category=document.get("category_name", "분류 없음"),
            phone=document.get("phone") or "전화번호 없음",
            address=document.get("address_name") or "주소 없음",
            road_address=(
                document.get("road_address_name")
                or document.get("address_name")
                or "주소 없음"
            ),
            place_url=document.get("place_url") or "링크 없음",
        )
        restaurants.append(restaurant)

    if not restaurants:
        raise RuntimeError(
            f"'{city} 맛집' 검색 결과가 없습니다."
        )

    return restaurants


def print_recommendation(
    recommendation: TravelRecommendation,
) -> None:
    """Gemini 여행지 추천 결과를 출력한다."""

    print("\n[1단계: Gemini 여행지 추천 결과]")
    print(f"추천 도시: {recommendation.recommended_city}")
    print(f"예상 날씨: {recommendation.weather}")
    print("행사·축제 후보:")

    for number, event in enumerate(
        recommendation.events,
        start=1,
    ):
        print(f"  {number}. {event}")

    print(f"추천 이유: {recommendation.reason}")


def print_restaurants(
    city: str,
    restaurants: list[Restaurant],
) -> None:
    """Kakao 음식점 검색 결과를 출력한다."""

    print(f"\n[2단계: Kakao Local API {city} 음식점 검색 결과]")

    for number, restaurant in enumerate(
        restaurants,
        start=1,
    ):
        print(f"\n{number}. {restaurant.name}")
        print(f"   분류: {restaurant.category}")
        print(f"   전화: {restaurant.phone}")
        print(f"   주소: {restaurant.road_address}")
        print(f"   지도: {restaurant.place_url}")

def save_results(
    travel_date: str,
    recommendation: TravelRecommendation,
    restaurants: list[Restaurant],
) -> tuple[Path, Path]:
    """여행 추천 결과를 JSON과 Markdown 파일로 저장한다."""

    results_directory = Path("results")
    results_directory.mkdir(exist_ok=True)

    result_data = {
        "travel_date": travel_date,
        "recommendation": recommendation.model_dump(),
        "restaurants": [
            restaurant.model_dump()
            for restaurant in restaurants
        ],
    }

    json_path = results_directory / f"travel_plan_{travel_date}.json"
    markdown_path = (
        results_directory / f"travel_plan_{travel_date}.md"
    )

    json_text = json.dumps(
        result_data,
        ensure_ascii=False,
        indent=2,
    )
    json_path.write_text(
        json_text,
        encoding="utf-8",
    )

    markdown_lines = [
        f"# {travel_date} 국내 여행 추천 결과",
        "",
        "## 1. Gemini 여행지 추천",
        "",
        f"- 추천 도시: {recommendation.recommended_city}",
        f"- 예상 날씨: {recommendation.weather}",
        f"- 추천 이유: {recommendation.reason}",
        "",
        "### 행사·축제 후보",
        "",
    ]

    for event in recommendation.events:
        markdown_lines.append(f"- {event}")

    markdown_lines.extend(
        [
            "",
            "## 2. Kakao Local API 음식점 검색 결과",
            "",
        ]
    )

    for number, restaurant in enumerate(
        restaurants,
        start=1,
    ):
        markdown_lines.extend(
            [
                f"### {number}. {restaurant.name}",
                "",
                f"- 분류: {restaurant.category}",
                f"- 전화: {restaurant.phone}",
                f"- 주소: {restaurant.road_address}",
                f"- 카카오맵: {restaurant.place_url}",
                "",
            ]
        )

    markdown_text = "\n".join(markdown_lines)

    markdown_path.write_text(
        markdown_text,
        encoding="utf-8",
    )

    return json_path, markdown_path

def main() -> None:
    """CLI 입력을 받아 여행지와 음식점을 추천한다."""

    parser = argparse.ArgumentParser(
        description="여행 날짜에 맞는 국내 여행지와 음식점을 추천합니다."
    )
    parser.add_argument(
        "-date",
        "--date",
        required=True,
        type=validate_date,
        help="여행 날짜를 YYYY-MM-DD 형식으로 입력하세요.",
    )

    args = parser.parse_args()

    print("국내 여행 추천 프로그램")
    print(f"입력한 여행 날짜: {args.date}")
    print("Gemini가 여행지를 추천하고 있습니다.")

    try:
        client = create_gemini_client()

        recommendation = recommend_destination(
            client,
            args.date,
        )
        print_recommendation(recommendation)

        city = recommendation.recommended_city

        print(f"\nKakao에서 '{city} 맛집'을 검색하고 있습니다.")

        restaurants = search_restaurants(city)
        print_restaurants(city, restaurants)
        json_path, markdown_path = save_results(
            args.date,
            recommendation,
            restaurants,
        )

        print("\n[3단계: 결과 파일 저장 완료]")
        print(f"JSON 파일: {json_path}")
        print(f"Markdown 파일: {markdown_path}")        
    except Exception as error:
        print(f"\n오류가 발생했습니다: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()