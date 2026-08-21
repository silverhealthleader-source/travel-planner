A1-2 국내 여행 추천 프로그램

사용자가 입력한 여행 날짜를 바탕으로 Gemini API가 국내 여행지를 추천하고, 추천 도시를 Kakao Local API에 자동 전달하여 음식점 5곳을 검색하는 CLI 기반 Python 프로그램입니다.

여행 추천 결과와 음식점 정보는 터미널에 출력되며 results 폴더에 JSON과 Markdown 파일로 자동 저장됩니다.

1. 주요 기능

YYYY-MM-DD 형식의 여행 날짜 입력 및 검증

Gemini API를 활용한 국내 여행지 추천

Pydantic을 활용한 구조화 JSON 검증

JSON 검증 실패 시 최대 1회 재요청

추천 도시명을 Kakao 검색어로 자동 전달

Kakao Local API로 음식점 5곳 검색

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

추천 도시명을 Kakao Local API에 전달합니다.

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

6. 실행 방법

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

같은 날짜로 프로그램을 다시 실행하면 기존 결과 파일이 새로운 결과로 갱신됩니다.

9. 입력 검증과 오류 처리

날짜 형식 오류

날짜는 YYYY-MM-DD 형식으로 입력해야 합니다.

API 키 누락

.env에 API 키가 없으면 어떤 환경변수가 누락되었는지 안내하고 프로그램을 종료합니다.

Gemini JSON 오류

Gemini 응답이 지정한 JSON 구조와 맞지 않으면 한 번만 재요청합니다. 두 번째 검증도 실패하면 오류 내용을 출력하고 종료합니다.

Kakao API 오류

인증 실패, 연결 오류 또는 시간 초과가 발생하면 오류 내용을 출력하고 종료합니다. API 요청 시간 제한은 10초입니다.

검색 결과 없음

추천 도시의 음식점 검색 결과가 없으면 안내 메시지를 출력하고 종료합니다.

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