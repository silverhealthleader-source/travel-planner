A1-2 국내 여행 추천 프로그램

사용자가 입력한 여행 날짜를 바탕으로 Gemini API가 국내 여행지를 추천하고, 추천 도시를 Kakao Local API에 자동 전달하여 음식점 5곳을 검색하는 CLI 기반 Python 프로그램입니다.

여행 추천 결과와 음식점 정보는 터미널에 출력되며 results 폴더에 JSON과 Markdown 파일로 자동 저장됩니다.

1. 주요 기능

YYYY-MM-DD 형식의 여행 날짜 입력 및 검증

Gemini API를 활용한 국내 여행지 추천

Pydantic을 활용한 구조화 JSON 검증

JSON 검증 실패 시 최대 1회 재요청

추천 도시명을 중심 지역 키워드로 정규화한 뒤 Kakao 검색어로 자동 전달

Kakao Local API로 음식점 5곳 검색

MapSearchAdapter 계약과 KakaoLocalAdapter 구현체를 이용한 지도 API 추상화

음식점명, 분류, 전화번호, 주소, 카카오맵 링크 출력

JSON 및 Markdown 결과 파일 자동 저장

API 키 누락 및 API 요청 오류 안내

UTF-8 인코딩을 적용한 한글 결과 저장

2. 사용 기술

Python 3.10 이상

Google Gemini API

Kakao Local REST API

google-genai

requests

python-dotenv

Pydantic

Git·GitHub

Visual Studio Code

Windows PowerShell

3. 프로그램 처리 흐름

사용자가 여행 날짜를 입력합니다.

날짜가 YYYY-MM-DD 형식인지 검사합니다.

.env에서 Gemini API 키를 불러옵니다.

Gemini가 추천 도시, 예상 날씨, 행사 후보, 추천 이유를 생성합니다.

Pydantic이 Gemini의 JSON 구조를 검사합니다.

JSON 검증 실패 시 한 번만 다시 요청합니다.

추천 도시명에서 특별시·광역시·특별자치도·시·군·구 등의 행정구역 표현을 정리하여 중심 검색 키워드를 생성합니다.

MapSearchAdapter 계약을 통해 KakaoLocalAdapter에 정규화된 검색 요청을 전달합니다.

해당 도시의 음식점 5곳을 검색합니다.

터미널에 전체 결과를 출력합니다.

JSON과 Markdown 파일을 results 폴더에 저장합니다.

4. 설치 방법

4-1. 저장소 내려받기

git clone 저장소주소
cd travel-planner

4-2. 가상환경 만들기

python -m venv .venv

4-3. 가상환경 Python 확인

.\.venv\Scripts\python.exe --version

4-4. 필수 패키지 설치

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

5. API 키 설정

프로젝트 최상위 폴더에 .env 파일을 만들고 다음 변수명을 작성합니다.

GEMINI_API_KEY=본인의_Gemini_API_키
KAKAO_REST_API_KEY=본인의_Kakao_REST_API_키

주의사항:

실제 API 키는 README에 작성하지 않습니다.

.env 파일은 GitHub에 올리지 않습니다.

API 키를 화면 캡처나 실행 로그에 노출하지 않습니다.

Kakao 키는 JavaScript 키가 아닌 REST API 키를 사용합니다.

.env.example에는 변수명만 작성하고 실제 키는 넣지 않습니다.

환경변수를 사용하는 이유는 다음과 같습니다.

- 보안: API 키를 소스코드와 문서에서 분리하여 실수로 공개되는 위험을 줄입니다.
- 운영 관리: 개발·테스트·배포 환경에서 코드를 수정하지 않고 서로 다른 키를 사용할 수 있습니다.
- 버전관리 회피: `.env`를 `.gitignore`에 등록하여 실제 키가 Git 커밋과 GitHub 기록에 포함되지 않도록 합니다.

6. 실행 방법

사용 가능한 인자와 사용법을 먼저 확인할 수 있습니다.

.\.venv\Scripts\python.exe .\travel_planner.py --help

.\.venv\Scripts\python.exe .\travel_planner.py -date "2026-10-15"

또는 다음 형식을 사용할 수 있습니다.

.\.venv\Scripts\python.exe .\travel_planner.py --date "2026-10-15"

7. 실행 결과 예시

국내 여행 추천 프로그램
입력한 여행 날짜: 2026-10-15
Gemini가 여행지를 추천하고 있습니다.

[1단계: Gemini 여행지 추천 결과]
추천 도시: 경주
예상 날씨: 10월 중순의 일반적인 가을 날씨
행사·축제 후보:
  1. 가을 행사 후보 - 개최 여부 확인 필요
추천 이유: 역사 문화와 가을 풍경을 함께 즐길 수 있습니다.

Kakao에서 '경주 맛집'을 검색하고 있습니다.

[2단계: Kakao Local API 경주 음식점 검색 결과]
1. 음식점명
   분류: 음식점
   전화: 000-000-0000
   주소: 경상북도 경주시 예시 주소
   지도: 카카오맵 장소 링크

[3단계: 결과 파일 저장 완료]
JSON 파일: results\travel_plan_2026-10-15.json
Markdown 파일: results\travel_plan_2026-10-15.md

실행할 때마다 Gemini의 추천 도시와 Kakao 검색 결과가 달라질 수 있습니다.

8. 결과 파일

프로그램 실행 후 results 폴더에 다음 파일이 생성됩니다.

results/travel_plan_2026-10-15.json
results/travel_plan_2026-10-15.md

JSON 파일에는 여행 날짜, 추천 정보, 음식점 5곳이 구조적으로 저장됩니다. Markdown 파일에는 사람이 읽기 편한 여행 추천 보고서가 저장됩니다.

같은 날짜로 프로그램을 다시 실행하면 기존 JSON을 Pydantic으로 검증합니다. 검증에 성공하면 Gemini와 Kakao Local API 호출을 생략하고 캐시 결과를 사용하며, 캐시가 없거나 손상된 경우에만 API를 다시 호출합니다.

9. 입력 검증과 오류 처리

날짜 형식 오류

날짜는 YYYY-MM-DD 형식으로 입력해야 합니다.

API 키 누락

.env에 API 키가 없으면 어떤 환경변수가 누락되었는지 안내하고 프로그램을 종료합니다.

Gemini JSON 오류

Gemini 응답이 지정한 JSON 구조와 맞지 않으면 한 번만 재요청합니다. 두 번째 검증도 실패하면 오류 내용을 출력하고 종료합니다.

Kakao API 오류

인증 실패, 연결 오류 또는 시간 초과가 발생하면 `errors` 목록에 단계·유형·메시지를 기록합니다. 음식점 정보는 `데이터 없음`으로 처리하고 가능한 경우 최종 리포트 생성을 계속합니다. API 요청 시간 제한은 10초입니다.

검색 결과 없음

추천 도시의 음식점 검색 결과가 없으면 `EMPTY_RESULT` 오류를 기록하고 음식점 정보를 `데이터 없음`으로 표시한 뒤 최종 리포트 생성을 계속합니다. 사용자는 더 넓은 지역명이나 인접 도시로 날짜를 바꾸어 다시 실행할 수 있습니다.

10. 정보 확인 주의사항

Gemini가 생성한 날씨는 실시간 기상예보가 아니라 계절상 일반적인 예상입니다.

행사·축제 정보는 후보이며 실제 개최 여부는 공식 홈페이지에서 확인해야 합니다.

음식점 정보는 Kakao Local API 검색 시점의 결과입니다.

방문 전 영업 여부, 휴무일, 전화번호를 다시 확인해야 합니다.

생성형 AI 답변 중 중요한 정보는 별도로 검증해야 합니다.

11. 보안 설정

.gitignore를 사용하여 다음 항목을 Git에서 제외합니다.

.env

.venv

__pycache__

*.pyc

로컬 백업 Python 파일

보안 확인 명령어:

git check-ignore -v .env

실제 API 키는 코드, README, 결과 파일, 캡처 이미지에 포함하지 않습니다.

12. 구현 완료 현황

Python 및 Git 개발환경 확인

Kakao REST API 키 발급

Gemini API 키 발급

가상환경 생성 및 필수 패키지 설치

날짜 형식 검증

Gemini API 연결

Gemini 구조화 JSON 여행지 추천

JSON 검증 실패 시 1회 재요청

Kakao Local API 음식점 검색

Gemini 추천 도시와 Kakao 검색 자동 연결

음식점 5곳 정보 출력

JSON 결과 파일 저장

Markdown 결과 파일 저장

API 키 Git 제외 및 보안 설정

requirements.txt 작성

13. 핵심 학습 내용

CLI 명령행 인자 처리

함수와 클래스 활용

환경변수를 이용한 API 키 관리

외부 API 요청과 응답 처리

Pydantic 데이터 구조 검증

JSON 및 Markdown 파일 저장

UTF-8 한글 인코딩

예외 처리와 제한적 재시도

기능 단위 Git 커밋

생성형 AI 결과의 사실 확인 필요성
## 보너스 과제: 결과 캐싱

같은 여행 날짜로 프로그램을 다시 실행할 때 기존에 저장된 원본 JSON 파일을 먼저 확인합니다.

기존 JSON 파일이 있고 내부 데이터가 정상적으로 검증되면 Gemini API와 Kakao Local API를 다시 호출하지 않고 저장된 결과를 사용합니다. 기존 데이터로 JSON과 Markdown 여행 리포트를 다시 생성할 수 있습니다.

### 캐싱 실행 방법

    .\.venv\Scripts\python.exe .\travel_planner.py -date "2026-10-15"

같은 날짜의 JSON이 존재하면 다음 메시지가 표시됩니다.

    저장된 원본 JSON을 발견했습니다.
    Gemini와 Kakao Local API 호출을 건너뜁니다.

### 캐싱 처리 순서

1. `results/travel_plan_YYYY-MM-DD.json` 파일의 존재 여부를 확인합니다.
2. 저장된 여행 날짜가 입력 날짜와 같은지 확인합니다.
3. 추천 결과와 음식점 데이터를 Pydantic 모델로 다시 검증합니다.
4. 데이터가 정상이면 외부 API 호출을 생략합니다.
5. 기존 데이터를 사용하여 Markdown 리포트를 재생성합니다.
6. JSON 파일이 없거나 손상된 경우에만 Gemini 및 Kakao API를 다시 호출합니다.

### 캐싱의 장점

- 외부 API 호출 횟수를 줄일 수 있습니다.
- 동일 날짜 재실행 속도가 빨라집니다.
- 불필요한 API 사용량과 비용을 줄일 수 있습니다.
- 저장된 데이터도 다시 검증하므로 잘못된 캐시 사용을 방지할 수 있습니다.

## 14. Gemini 구조화 JSON 스키마

Gemini 1차 추천은 `TravelRecommendation` Pydantic 모델을 응답 스키마로 지정합니다.

```json
{
  "recommended_city": "경상북도 경주시",
  "weather": "계절상 일반적인 예상 날씨와 옷차림 안내",
  "events": ["행사 후보 - 실제 개최 여부 확인 필요"],
  "reason": "추천 이유"
}
```

스키마를 강제하면 필수 키와 자료형을 자동으로 검사할 수 있고, 검증된 `recommended_city`를 다음 Kakao 검색 단계에 안전하게 재사용할 수 있습니다. 또한 JSON 저장과 Markdown 리포트 생성에서도 동일한 구조를 사용할 수 있습니다.

## 15. 주요 함수와 외부 인터페이스

| 함수·클래스 | 입력 | 출력·부작용 |
|---|---|---|
| `validate_date(date_text)` | 날짜 문자열 | 검증된 `YYYY-MM-DD` 문자열 또는 인자 오류 |
| `recommend_destination(client, travel_date)` | Gemini 클라이언트, 날짜 | 검증된 `TravelRecommendation` |
| `normalize_city_keyword(city)` | Gemini 추천 지역명 | Kakao 검색용 중심 지역 키워드 |
| `MapSearchAdapter` | 도시 검색 계약 | 지도 공급자 교체를 위한 공통 인터페이스 |
| `KakaoLocalAdapter.search_restaurants(city)` | 추천 지역명 | 최대 5개의 `Restaurant` 목록 |
| `search_restaurants(city, adapter)` | 도시명, 지도 어댑터 | 어댑터가 반환한 표준 음식점 목록 |
| `generate_final_report(...)` | 추천·음식점·오류 데이터 | Gemini가 생성한 Markdown 문자열 |
| `load_cached_results(travel_date)` | 날짜 | 검증된 캐시 또는 `None` |
| `save_results(...)` | 전체 결과 | JSON·Markdown 경로, 파일 저장 부작용 |

## 16. 지도 API 어댑터 구조

핵심 로직이 Kakao의 URL과 응답 필드에 직접 묶이지 않도록 지도 검색 기능을 분리했습니다.

- `MapSearchAdapter`: 지도 서비스가 구현해야 하는 `search_restaurants(city)` 계약을 정의합니다.
- `KakaoLocalAdapter`: Kakao 인증 헤더, GET 요청, 응답 필드 변환을 담당합니다.
- `search_restaurants()`: 전달받은 어댑터를 호출하며, 어댑터가 없으면 Kakao 구현체를 기본값으로 사용합니다.
- 모든 공급자는 공급자 고유 응답을 공통 `Restaurant` 모델로 변환해야 합니다.

향후 다른 지도 API를 사용하려면 `MapSearchAdapter` 계약을 따르는 새 클래스를 만들고 호출 시 해당 객체를 전달하면 됩니다. 추천·리포트·저장 로직은 변경할 필요가 없습니다.

## 17. 추천 도시 키워드 정규화

Gemini가 행정구역이 포함된 지명을 반환해도 검색 품질이 떨어지지 않도록 `normalize_city_keyword()`를 먼저 실행합니다.

| 추천 지역명 | 정규화 결과 | 최종 검색어 |
|---|---|---|
| `제주특별자치도` | `제주` | `제주 맛집` |
| `서울특별시` | `서울` | `서울 맛집` |
| `부산광역시` | `부산` | `부산 맛집` |
| `경상북도 경주시` | `경주` | `경주 맛집` |
| `전라남도 여수시` | `여수` | `여수 맛집` |

여러 단어로 구성된 지명은 시·군을 우선 선택하고, 시·군이 없으면 구 또는 마지막 지역명을 사용합니다. 공백을 정리하고 행정구역 접미사를 제거한 결과에 `맛집`을 붙여 Kakao에 전달합니다.

## 18. 외부 API 요청 방식과 GET/POST 선택 근거

### Kakao Local API: GET

- 엔드포인트: `https://dapi.kakao.com/v2/local/search/keyword.json`
- 검색어, 음식점 분류 코드, 결과 개수, 정렬 방식은 쿼리 파라미터로 전달합니다.
- 서버의 장소 데이터를 조회하는 읽기 작업이며 새로운 데이터를 생성하거나 수정하지 않으므로 GET을 사용합니다.
- 인증은 `Authorization: KakaoAK {REST_API_KEY}` 헤더로 전달합니다.

### Gemini API: SDK의 콘텐츠 생성 요청

- 코드에서는 `client.models.generate_content()`를 사용합니다.
- 프롬프트, 응답 스키마, temperature 같은 생성 설정은 요청 본문으로 전달해야 하므로 SDK 내부에서는 콘텐츠 생성용 POST 방식의 요청으로 처리됩니다.
- Gemini 1차 호출은 JSON 스키마가 적용된 여행 추천을 만들고, 2차 호출은 검증된 추천·음식점·오류 데이터를 바탕으로 Markdown 리포트를 만듭니다.

프로그램은 Kakao 조회에 `requests.get()`을 직접 사용하지만 Gemini는 공식 SDK에 요청 구성을 맡깁니다. 따라서 Gemini URL이나 인증 헤더를 코드에 직접 작성하지 않습니다.

## 19. API 키를 환경변수로 관리하는 이유

API 키는 인증 정보이므로 일반 설정값과 분리해야 합니다.

- 보안: 키를 Python 코드, README, 결과 파일, 캡처 이미지에서 분리합니다.
- 운영: 컴퓨터나 실행 환경이 달라져도 `.env` 값만 변경하고 코드는 동일하게 유지합니다.
- 버전관리: `.env`는 `.gitignore`로 제외하여 GitHub 커밋에 실제 키가 포함되지 않게 합니다.
- 공유: `.env.example`에는 변수명만 제공하여 다른 사용자가 자신의 키를 입력하게 합니다.

코드는 프로젝트 루트의 `.env`를 `load_dotenv(dotenv_path=Path(".env"), override=True)`로 읽습니다. 변수명은 정확히 `GEMINI_API_KEY`, `KAKAO_REST_API_KEY`를 사용합니다.

## 20. 401·403 인증 오류 디버깅 체크리스트

### 공통 확인

1. 터미널 위치가 프로젝트 루트인지 `Get-Location`으로 확인합니다.
2. `.env` 파일명이 `.env.txt`가 아닌지 확인합니다.
3. 변수명이 `GEMINI_API_KEY`, `KAKAO_REST_API_KEY`와 정확히 일치하는지 확인합니다.
4. 실제 키 앞뒤에 불필요한 공백이나 설명 문구가 없는지 확인합니다.
5. 실제 키를 로그에 출력하지 말고 `bool(os.getenv(...))` 결과만 확인합니다.

### Kakao 401

- JavaScript 키나 Admin 키가 아니라 REST API 키인지 확인합니다.
- 인증 헤더가 `Authorization: KakaoAK 실제키` 형식인지 확인합니다.
- 키가 삭제·재발급되어 기존 키가 만료되지 않았는지 확인합니다.

### Kakao 403

- Kakao Developers에서 앱이 정상 상태인지 확인합니다.
- 앱에서 Local API 사용이 허용되는지와 관련 권한·사용 제한을 확인합니다.
- 플랫폼 또는 도메인 제한을 설정했다면 현재 사용 환경이 등록 조건과 맞는지 확인합니다.
- 요청량 제한이나 정책 제한 여부를 개발자 콘솔에서 확인합니다.

### Gemini 401·403

- Gemini API 키가 Google AI Studio에서 정상 발급되었는지 확인합니다.
- 해당 프로젝트에서 Gemini API 사용이 가능한지 확인합니다.
- 키 제한, 할당량, 모델 접근 권한을 확인합니다.

오류는 `errors` 목록과 터미널에 기록하며 실제 API 키는 기록하지 않습니다.

## 21. 오류 데이터 표준 형식

프로그램은 단계별 오류를 다음 형식으로 누적하여 JSON과 Markdown에 함께 저장합니다.

```json
{
  "step": "place_search",
  "type": "API_ERROR",
  "message": "사용자에게 필요한 오류 설명"
}
```

- `step`: 오류 발생 단계 (`place_search`, `final_report` 등)
- `type`: 오류 유형 (`API_ERROR`, `EMPTY_RESULT` 등)
- `message`: 키를 제외한 진단 메시지

## 22. 재시도·대체 처리 정책

- Gemini 1차 JSON이 비었거나 스키마 검증에 실패하면 같은 스키마 조건으로 한 번만 재요청합니다.
- 두 번째 검증도 실패하면 무한 반복하지 않고 오류를 반환합니다.
- Kakao 검색이 실패하거나 0건이면 음식점 목록을 빈 배열로 두고 오류를 기록한 뒤 리포트 생성을 계속합니다.
- Gemini 최종 리포트 생성이 실패하면 오류를 기록하고 검증된 데이터로 기본 Markdown 리포트를 만듭니다.
- 파일 저장이 실패하면 최상위 예외 처리에서 오류를 표시합니다. 사용자는 `results` 폴더 쓰기 권한과 디스크 공간을 확인한 뒤 다시 실행합니다.

## 23. 캐시 유효성 및 만료 정책

현재 캐시는 자동 만료 시간을 두지 않습니다. 같은 날짜의 JSON 파일이 다음 기준을 모두 만족하면 유효한 캐시로 사용합니다.

1. 파일명이 입력 날짜와 대응합니다.
2. JSON 내부의 `travel_date`가 입력 날짜와 같습니다.
3. `recommendation`이 `TravelRecommendation` 모델 검증을 통과합니다.
4. 모든 음식점 항목이 `Restaurant` 모델 검증을 통과합니다.

검증 실패 시 캐시를 사용하지 않고 API를 다시 호출합니다. 최신 추천이나 음식점 정보가 필요하면 해당 날짜의 JSON·Markdown 파일을 별도로 백업한 뒤 삭제하고 다시 실행합니다.

## 24. 네이토 사전평가 보완 사항

| 평가 항목 | 보완 내용 |
|---|---|
| #8 | `MapSearchAdapter` 계약과 `KakaoLocalAdapter` 구현체로 지도 API를 분리했습니다. |
| #10 | Kakao GET과 Gemini 생성 요청 방식의 선택 근거 및 엔드포인트를 문서화했습니다. |
| #12 | Kakao·Gemini 401/403 원인과 안전한 점검 순서를 추가했습니다. |
| #13 | 환경변수 사용 이유를 보안·운영·버전관리 관점에서 설명했습니다. |
| #17 | 추천 지명의 행정구역 표현을 중심 검색 키워드로 정규화하는 단계를 추가했습니다. |
