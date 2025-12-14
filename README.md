# 파일 확장자 차단 (File Extension Blocking)

## 과제 설명
파일 첨부 시 보안상 위험할 수 있는 특정 확장자(exe, sh 등)를 차단하는 관리 페이지입니다.
고정된 확장자를 차단하거나, 커스텀 확장자를 추가하여 차단할 수 있습니다.

## 기술 스택 (Tech Stack)
- **Backend**: Python 3.10+, FastAPI
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 주요 기능 (Features)
1. **고정 확장자 차단**
   - `bat`, `cmd`, `com`, `cpl`, `exe`, `scr`, `js`
   - 체크박스를 통해 차단 여부를 설정하며, DB에 저장됩니다.

2. **커스텀 확장자 차단**
   - **추가**: 최대 20자, 영문/숫자만 입력 가능 (한글/특수문자 차단).
   - **삭제**: 개별 삭제 및 '전체 삭제' 기능 지원.
   - **제한**: 최대 200개까지 등록 가능. 중복 등록 불가.
   - **조회**: 등록된 확장자는 태그 형태로 시각화되어 표시됩니다.

## 설치 및 실행 (Installation & Run)

### 1. 환경 설정
Python이 설치되어 있어야 합니다.

```bash
# 의존성 설치
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

### 3. 접속
브라우저에서 아래 주소로 접속합니다.
[http://localhost:8001/static/index.html](http://localhost:8001/static/index.html)

## API 명세
- `GET /api/extensions`: 전체 확장자 목록 조회
- `PATCH /api/fixed-extensions/{name}`: 고정 확장자 상태 변경
- `POST /api/custom-extensions`: 커스텀 확장자 추가
- `DELETE /api/custom-extensions/{name}`: 커스텀 확장자 삭제
- `DELETE /api/custom-extensions`: 커스텀 확장자 전체 삭제

## 프로젝트 구조
```
block-extension-exp/
├── main.py              # FastAPI 서버 및 API 엔드포인트
├── database.py          # DB 연결 및 초기화
├── requirements.txt     # 파이썬 의존성 목록
├── extensions.db        # SQLite 데이터베이스 (자동 생성)
└── static/              # 프론트엔드 정적 파일
    ├── index.html       # 메인 페이지
    ├── style.css        # 스타일시트
    └── script.js        # 프론트엔드 로직
```
