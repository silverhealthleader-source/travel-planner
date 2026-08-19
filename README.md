# A1-2 국내 여행 추천 프로그램

## 1. 프로그램 개요

사용자가 입력한 여행 날짜를 기반으로 Gemini API가 국내 여행지를 추천하고, Kakao Local API가 추천 지역의 맛집을 검색한 뒤 최종 여행 리포트를 생성하는 CLI 기반 Python 프로그램입니다.

## 2. 주요 기능

- `-date "YYYY-MM-DD"` 형식의 여행 날짜 입력
- 날짜 형식 검증
- Gemini API를 활용한 국내 여행지 추천
- 구조화된 JSON 추천 결과 생성
- Kakao Local API를 활용한 맛집 검색
- 최종 여행 리포트 Markdown 생성
- 원본 JSON과 최종 리포트를 `results/` 폴더에 저장
- API 및 JSON 파싱 오류 처리

## 3. 사용 API

- Google Gemini API
- Kakao Local REST API

## 4. API 키 보안

API 키는 코드에 직접 작성하지 않고 `.env` 파일에 저장합니다.

`.env` 파일은 `.gitignore`에 등록하여 GitHub에 업로드되지 않도록 관리합니다.

실제 API 키는 README, 실행 로그, 결과 파일 및 화면 캡처에 포함하지 않습니다.

## 5. 현재 개발 상태

- [x] Python 및 Git 개발환경 확인
- [x] Kakao REST API 키 발급
- [x] 카카오맵 API 활성화
- [x] Kakao Local API 맛집 검색 테스트
- [x] CLI 날짜 입력 및 형식 검증
- [ ] Gemini API 연동
- [ ] Kakao Local API Python 연동
- [ ] 최종 Markdown 리포트 생성
- [ ] JSON 및 Markdown 결과 저장