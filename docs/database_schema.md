# 데이터베이스 구조 (Database Schema)

**file_extensions** (파일 확장자 관리)
| 컬럼명 | 타입 | 설명 |
|---|---|---|
| `name` | TEXT (PK) | 확장자 이름 (예: exe, bat, custom1) |
| `type` | VARCHAR | 확장자 유형 ('fixed' 또는 'custom') |
| `is_allowed` | BOOLEAN | 허용 여부 (0: 차단, 1: 허용) |
| `update_by` | VARCHAR | 수정자 (예: system, guest) |
| `update_at` | TIMESTAMP | 수정 일시 |
