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
    events: list[str] = Field(description="행사 또는 축제 후보 목록")
    reason: str = Field(description="해당 지역을 추천하는 이유")


class Restaurant(BaseModel):
    """Kakao Local API에서 사용할 음식점 정보."""

    name: str
    category: str
    phone: str
    address: str
    road_address: str
    place_url: str
    x: float | None = None
    y: float | None = None


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

    load_dotenv()
    api_key = os.getenv(variable_name)

    if not api_key:
        raise RuntimeError(
            f"{variable_name}가 설정되지 않았습니다. .env 파일을 확인하세요."
        )

    return api_key


def create_gemini_client() -> genai.Client:
    """Gemini API 클라이언트를 만든다."""

    return genai.Client(api_key=load_api_key("GEMINI_API_KEY"))


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

            return TravelRecommendation.model_validate_json(response.text)
        except (ValidationError, ValueError) as error:
            last_error = error

            if attempt == 1:
                print("JSON 검증에 실패하여 한 번 더 요청합니다.")

    raise RuntimeError(
        f"Gemini JSON 생성에 실패했습니다: {last_error}"
    )


def generate_final_report(
    client: genai.Client,
    travel_date: str,
    recommendation: TravelRecommendation,
    restaurants: list[Restaurant],
    errors: list[dict[str, str]],
) -> str:
    """추천 결과와 음식점 데이터를 이용해 최종 Markdown 리포트를 생성한다."""

    recommendation_data = json.dumps(
        recommendation.model_dump(),
        ensure_ascii=False,
        indent=2,
    )

    restaurant_data = json.dumps(
        [restaurant.model_dump() for restaurant in restaurants],
        ensure_ascii=False,
        indent=2,
    )

    error_data = json.dumps(
        errors,
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"""
다음 데이터를 이용하여 국내 여행 추천 리포트를 작성하세요.

여행 날짜:
{travel_date}

1차 여행지 추천 JSON:
{recommendation_data}

Kakao 음식점 검색 결과:
{restaurant_data}

오류 목록:
{error_data}

다음 조건을 반드시 지키세요.

1. 결과는 Markdown 문서만 출력하세요.
2. Markdown 코드 블록 기호는 사용하지 마세요.
3. 제공된 데이터에 없는 음식점이나 행사를 새로 만들지 마세요.
4. 음식점 검색 결과가 빈 목록이면 '데이터 없음'으로 표시하세요.
5. 오류 목록이 비어 있으면 '오류 없음'으로 표시하세요.
6. 아래 제목을 정확히 모두 포함하세요.

# {travel_date} 국내 여행 추천 리포트
## 추천 지역
## 추천 이유
## 날씨 요약
## 행사/축제
## 맛집 추천
## 1일 일정 제안
## 오류 요약(errors)

1일 일정은 오전, 오후, 저녁으로 나누어 작성하세요.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
        ),
    )

    if not response.text:
        raise ValueError("Gemini 최종 리포트 응답 내용이 비어 있습니다.")

    return response.text.strip()


def search_restaurants(city: str) -> list[Restaurant]:
    """추천 도시의 음식점 5곳을 Kakao Local API로 검색한다."""

    kakao_api_key = load_api_key("KAKAO_REST_API_KEY")
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
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

    documents = response.json().get("documents", [])
    restaurants: list[Restaurant] = []

    for document in documents:
        restaurants.append(
            Restaurant(
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
                x=float(document["x"]) if document.get("x") else None,
                y=float(document["y"]) if document.get("y") else None,               
            )
        )

    if not restaurants:
        return []

    return restaurants

def load_cached_results(
    travel_date: str,
) -> tuple[
    TravelRecommendation,
    list[Restaurant],
    list[dict[str, str]],
] | None:
    """같은 날짜의 원본 JSON이 있으면 검증 후 캐시 결과를 반환한다."""

    json_path = Path("results") / f"travel_plan_{travel_date}.json"

    if not json_path.exists():
        return None

    try:
        result_data = json.loads(json_path.read_text(encoding="utf-8"))

        if result_data.get("travel_date") != travel_date:
            raise ValueError("캐시 파일의 여행 날짜가 일치하지 않습니다.")

        recommendation = TravelRecommendation.model_validate(
            result_data["recommendation"]
        )
        restaurants = [
            Restaurant.model_validate(item)
            for item in result_data["restaurants"]
        ]
        errors = result_data.get("errors", [])

        return recommendation, restaurants, errors

    except (KeyError, TypeError, ValueError, json.JSONDecodeError, ValidationError) as error:
        print(f"저장된 JSON을 사용할 수 없어 API를 다시 호출합니다: {error}")
        return None


def print_recommendation(recommendation: TravelRecommendation) -> None:
    """Gemini 여행지 추천 결과를 출력한다."""

    print("\n[1단계: Gemini 여행지 추천 결과]")
    print(f"추천 도시: {recommendation.recommended_city}")
    print(f"예상 날씨: {recommendation.weather}")
    print("행사·축제 후보:")

    for number, event in enumerate(recommendation.events, start=1):
        print(f"  {number}. {event}")

    print(f"추천 이유: {recommendation.reason}")


def print_restaurants(
    city: str,
    restaurants: list[Restaurant],
) -> None:
    """Kakao 음식점 검색 결과를 출력한다."""

    print(f"\n[2단계: Kakao Local API {city} 음식점 검색 결과]")

    for number, restaurant in enumerate(restaurants, start=1):
        print(f"\n{number}. {restaurant.name}")
        print(f"   분류: {restaurant.category}")
        print(f"   전화: {restaurant.phone}")
        print(f"   주소: {restaurant.road_address}")
        print(f"   지도: {restaurant.place_url}")


def save_results(
    travel_date: str,
    recommendation: TravelRecommendation,
    restaurants: list[Restaurant],
    errors: list[dict[str, str]],
    report_markdown: str | None = None,         
) -> tuple[Path, Path]:
    """여행 추천 결과를 JSON과 Markdown 파일로 저장한다."""

    results_directory = Path("results")
    results_directory.mkdir(exist_ok=True)

    result_data = {
        "travel_date": travel_date,
        "recommendation": recommendation.model_dump(),
        "restaurants": [item.model_dump() for item in restaurants],
        "errors": errors,        
    }

    json_path = results_directory / f"travel_plan_{travel_date}.json"
    markdown_path = results_directory / f"travel_plan_{travel_date}.md"

    json_path.write_text(
        json.dumps(result_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    markdown_lines = [
        f"# {travel_date} 국내 여행 추천 리포트",
        "",
        "## 추천 지역",
        "",
        f"- {recommendation.recommended_city}",
        "",
        "## 추천 이유",
        "",
        recommendation.reason,
        "",
        "## 날씨 요약",
        "",
        recommendation.weather,
        "",
        "## 행사/축제",
        "",
    ]

    if recommendation.events:
        for event in recommendation.events:
            markdown_lines.append(f"- {event}")
    else:
        markdown_lines.append("- 데이터 없음")

    markdown_lines.extend(["", "## 맛집 추천", ""])

    if restaurants:
        for number, restaurant in enumerate(restaurants, start=1):
            markdown_lines.extend(
                [
                    f"### {number}. {restaurant.name}",
                    "",
                    f"- 분류: {restaurant.category}",
                    f"- 전화: {restaurant.phone}",
                    f"- 주소: {restaurant.road_address}",
                    f"- 카카오맵: {restaurant.place_url}",
                ]
            )

            if restaurant.x is not None and restaurant.y is not None:
                markdown_lines.append(
                    f"- 좌표: x={restaurant.x}, y={restaurant.y}"
                )

            markdown_lines.append("")
    else:
        markdown_lines.append("- 데이터 없음 (장소 검색 결과 0건)")

    dinner_place = (
        restaurants[0].name
        if restaurants
        else "현지 식당(검색 데이터 없음)"
    )

    markdown_lines.extend(
        [
            "",
            "## 1일 일정 제안",
            "",
            f"- 오전: {recommendation.recommended_city}의 대표 명소를 여유롭게 둘러봅니다.",
            "- 오후: 행사·축제 후보 또는 지역 문화거리를 방문합니다.",
            f"- 저녁: {dinner_place}에서 식사 후 일정을 마무리합니다.",
            "",
            "## 오류 요약(errors)",
            "",
        ]
    )

    if errors:
        for error_item in errors:
            markdown_lines.append(
                f"- [{error_item.get('step', 'unknown')}] "
                f"{error_item.get('type', 'ERROR')}: "
                f"{error_item.get('message', '')}"
            )
    else:
        markdown_lines.append("- 오류 없음")
    final_markdown = report_markdown or "\n".join(markdown_lines)

    markdown_path.write_text(
        final_markdown,
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

    errors: list[dict[str, str]] = []
    report_markdown: str | None = None

    try:
        cached_results = load_cached_results(args.date)

        if cached_results is not None:
            print("저장된 원본 JSON을 발견했습니다.")
            print("Gemini와 Kakao Local API 호출을 건너뜁니다.")
            recommendation, restaurants, cached_errors = cached_results
            errors.extend(cached_errors)
            city = recommendation.recommended_city
            cached_markdown_path = (
                Path("results") / f"travel_plan_{args.date}.md"
            )

            if cached_markdown_path.exists():
                report_markdown = cached_markdown_path.read_text(
                    encoding="utf-8"
                )            
        else:
            print("저장된 결과가 없어 API를 호출합니다.")
            print("Gemini가 여행지를 추천하고 있습니다.")
            client = create_gemini_client()
            recommendation = recommend_destination(client, args.date)
            city = recommendation.recommended_city
            print(f"\nKakao에서 '{city} 맛집'을 검색하고 있습니다.")

            try:
                restaurants = search_restaurants(city)
                if not restaurants:
                    errors.append(
                        {
                            "step": "place_search",
                            "type": "EMPTY_RESULT",
                            "message": f"0 results for query={city} 맛집",
                        }
                    )
                    print("검색 결과가 0건입니다.")
                    print("맛집 정보를 '데이터 없음'으로 처리합니다.")        

            except Exception as error:
                restaurants = []
                errors.append(
                    {
                        "step": "place_search",
                        "type": "API_ERROR",
                        "message": str(error),
                    }
                )

                print(f"Kakao Local API 오류: {error}")
                print("맛집 정보를 '데이터 없음'으로 처리합니다.")
                print("여행 리포트 생성을 계속 진행합니다.")
            print("\n[3/3] 최종 여행 리포트 생성 중(Gemini)...")

            try:
                report_markdown = generate_final_report(
                    client,
                    args.date,
                    recommendation,
                    restaurants,
                    errors,
                )
                print("최종 리포트 생성 완료")

            except Exception as error:
                errors.append(
                    {
                        "step": "final_report",
                        "type": "API_ERROR",
                        "message": str(error),
                    }
                )
                print(f"Gemini 최종 리포트 생성 오류: {error}")
                print("기본 리포트로 계속 진행합니다.")

        print_recommendation(recommendation)
        print_restaurants(
            recommendation.recommended_city,
            restaurants,
        )
        json_path, markdown_path = save_results(
            args.date,
            recommendation,
            restaurants,
            errors,
            report_markdown,
        )

        print("\n[3단계: 결과 파일 저장 완료]")
        print(f"JSON 파일: {json_path}")
        print(f"Markdown 파일: {markdown_path}")
    except Exception as error:
        print(f"\n오류가 발생했습니다: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
