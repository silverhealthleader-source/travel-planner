"""Gemini와 Kakao Local API를 활용한 국내 여행 추천 프로그램."""

import argparse
from datetime import datetime


def validate_date(date_text: str) -> str:
    """YYYY-MM-DD 형식의 날짜인지 확인한다."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "날짜는 YYYY-MM-DD 형식으로 입력하세요. 예: 2026-10-15"
        ) from error


def main() -> None:
    """CLI 입력을 받아 프로그램을 시작한다."""
    parser = argparse.ArgumentParser(
        description="여행 날짜에 맞는 국내 여행지를 추천합니다."
    )
    parser.add_argument(
        "-date",
        "--date",
        required=True,
        type=validate_date,
        help='여행 날짜를 YYYY-MM-DD 형식으로 입력하세요.',
    )

    args = parser.parse_args()

    print("국내 여행 추천 프로그램")
    print(f"입력한 여행 날짜: {args.date}")
    print("날짜 입력 검증이 완료되었습니다.")


if __name__ == "__main__":
    main()