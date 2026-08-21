"""Gemini와 Kakao Local API를 활용한 국내 여행 추천 프로그램."""

import argparse
import os
from datetime import datetime

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
        description="입력한 여행 시기의 일반적인 예상 날씨와 옷차림 안내"
    )
    events: list[str] = Field(
        description="여행 날짜 전후에 열릴 가능성이 있는 행사 또는 축제 후보"
    )
    reason: str = Field(
        description="해당 지역을 추천하는 구체적인 이유"
    )


def validate_date(date_text: str) -> str:
    """YYYY-MM-DD 형식의 날짜인지 확인한다."""

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "날짜는 YYYY-MM-DD 형식으로 입력하세요. 예: 2026-10-15"
        ) from error


def create_gemini_client() -> genai.Client:
    """환경변수의 Gemini API 키로 클라이언트를 만든다."""

    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."
        )

    return genai.Client(api_key=api_key)


def recommend_destination(
    client: genai.Client,
    travel_date: str,
) -> TravelRecommendation:
    """Gemini로 국내 여행지를 추천받고 JSON 구조를 검사한다."""

    prompt = f"""
당신은 대한민국 국내 여행 전문 가이드입니다.

여행 날짜는 {travel_date}입니다.
계절과 이동 편의성, 대표 볼거리, 먹거리 등을 고려하여
대한민국 국내 여행지 한 곳을 추천하세요.

다음 기준을 지켜 주세요.
1. 추천 지역은 대한민국 안에 있어야 합니다.
2. 날씨는 확정 예보가 아닌 계절상 일반적인 예상이라고 설명하세요.
3. 행사와 축제는 실제 개최 여부를 별도로 확인해야 하는 후보로 작성하세요.
4. 행사 정보마다 반드시 '확인 필요'라는 문구를 넣으세요.
5. 추천 이유는 초보 여행자도 이해하기 쉽게 작성하세요.
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

            return TravelRecommendation.model_validate_json(response.text)

        except (ValidationError, ValueError) as error:
            last_error = error

            if attempt == 1:
                print("JSON 검증에 실패하여 한 번 더 요청합니다.")

    raise RuntimeError(
        f"Gemini JSON 생성에 실패했습니다: {last_error}"
    )


def main() -> None:
    """CLI 입력을 받아 여행지를 추천한다."""

    parser = argparse.ArgumentParser(
        description="여행 날짜에 맞는 국내 여행지를 추천합니다."
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
        recommendation = recommend_destination(client, args.date)
    except Exception as error:
        print(f"오류가 발생했습니다: {error}")
        raise SystemExit(1) from error

    print("\n[Gemini 여행지 추천 결과]")
    print(f"추천 도시: {recommendation.recommended_city}")
    print(f"예상 날씨: {recommendation.weather}")
    print("행사·축제 후보:")

    for number, event in enumerate(recommendation.events, start=1):
        print(f"  {number}. {event}")

    print(f"추천 이유: {recommendation.reason}")


if __name__ == "__main__":
    main()