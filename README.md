# 파일 확장자 차단 (File Extension Blocking)

## 과제 설명
파일 첨부 시 보안상 위험할 수 있는 특정 확장자(exe, sh 등)를 차단하는 관리 페이지입니다.
고정된 확장자를 차단하거나, 커스텀 확장자를 추가하여 차단할 수 있습니다.

## 기술 스택 (Tech Stack)
- **Backend**: Python 3.10+, FastAPI
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 데이터베이스 구조 (Database Schema)
**1. fixed_extensions** (고정 확장자)
| 컬럼명 | 타입 | 설명 |
|---|---|---|
| `name` | TEXT (PK) | 확장자 이름 (예: exe, bat) |
| `is_checked` | INTEGER | 차단 여부 (0: 허용, 1: 차단) |

**2. custom_extensions** (커스텀 확장자)
| 컬럼명 | 타입 | 설명 |
|---|---|---|
| `name` | TEXT (PK) | 확장자 이름 (최대 20자) |

## 주요 기능 (Features)
1. **고정 확장자 차단**
   - `bat`, `cmd`, `com`, `cpl`, `exe`, `scr`, `js`
   - 체크박스를 통해 차단 여부를 설정하며, DB에 저장됩니다.

2. **커스텀 확장자 차단**
   - **추가**: 최대 20자, 영문/숫자만 입력 가능 (한글/특수문자 차단).
   - **삭제**: 개별 삭제 및 '전체 삭제' 기능 지원.
   - **제한**: 최대 200개까지 등록 가능. 중복 등록 불가.
   - **조회**: 등록된 확장자는 태그 형태로 시각화되어 표시됩니다.

## 개발 시 고려사항 (Considerations)
1. **데이터 무결성 및 보안**
   - **입력 검증**: 커스텀 확장자 추가 시 길이(20자) 및 형식(영문/숫자)을 엄격히 제한하여 잘못된 데이터나 스크립트 주입을 방지했습니다.
   - **중복 방지**: 이미 등록된 확장자는 중복 등록되지 않도록 처리했습니다.

2. **사용자 경험 (UX)**
   - **실시간 피드백**: 잘못된 입력이나 중복 시 즉각적인 알림(Alert)을 제공합니다.
   - **시각화**: 커스텀 확장자를 태그 형태로 보여주어 직관적으로 관리할 수 있게 했습니다.
   - **편의성**: 개별 삭제뿐만 아니라 '전체 삭제' 기능을 추가하여 테스트 및 초기화 편의성을 높였습니다.

3. **배포 및 확장성**
   - **환경 변수 지원**: `PORT` 환경 변수를 지원하여 Cloudtype 등 다양한 배포 환경에서 유연하게 동작하도록 했습니다.
   - **경량화**: FastAPI와 SQLite를 사용하여 가볍고 빠르게 동작하며, 별도의 복잡한 DB 설정 없이 바로 실행 가능합니다.

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
