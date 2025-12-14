# 데이터베이스 구조 (Database Schema)

**1. fixed_extensions** (고정 확장자)
| 컬럼명 | 타입 | 설명 |
|---|---|---|
| `name` | TEXT (PK) | 확장자 이름 (예: exe, bat) |
| `is_checked` | INTEGER | 차단 여부 (0: 허용, 1: 차단) |

**2. custom_extensions** (커스텀 확장자)
| 컬럼명 | 타입 | 설명 |
|---|---|---|
| `name` | TEXT (PK) | 확장자 이름 (최대 20자) |
