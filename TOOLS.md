# Tools

## 런타임·패키지 관리

| 이름 | 버전 | 용도 | 라이선스 | 로드·설치 방법 | 설치 필요 | 로컬 설치 여부 |
|---|---|---|---|---|---|---|
| Python | 3.15 (`requires-python >=3.15`) | 런타임 | PSF-2.0 | uv가 관리 (`uv python install 3.15`) | 예 | 예 (uv 관리) |
| uv | 0.13.6 | 의존성 설치·실행 (`uv sync`, `uv run`) | Apache-2.0 | https://docs.astral.sh/uv/ 설치 안내 | 예 (전역) | 예 |

## Python 의존성 (`uv.lock` 고정)

| 이름 | 버전 | 용도 | 라이선스 | 로드·설치 방법 | 설치 필요 | 로컬 설치 여부 |
|---|---|---|---|---|---|---|
| fastapi[standard] | 0.165.0 | API 서버 | MIT | `uv sync` | 예 (.venv) | 예 |
| pydantic | 2.14.4 | 데이터 모델 검증 (fastapi 의존성) | MIT | `uv sync` | 예 (.venv) | 예 |
| httpx | 0.28.1 | `TestClient` 백엔드 | BSD-3-Clause | `uv sync` | 예 (.venv) | 예 |
| pytest | 9.2.0 | 테스트 | MIT | `uv sync` | 예 (.venv) | 예 |

## CI (GitHub Actions, `.github/workflows/ci.yml`)

| 이름 | 버전 (커밋 SHA 고정) | 용도 | 라이선스 | 설치 필요 |
|---|---|---|---|---|
| actions/checkout | v7.0.1 (`3d3c42e5aac5ba805825da76410c181273ba90b1`) | 소스 체크아웃 | MIT | 아니오 (러너가 로드) |
| astral-sh/setup-uv | v10.3.3 (`68559e99cc807c1eb7e9238fd43a15bba460eec2`) | 러너에 uv·Python 설치, 캐시 | MIT | 아니오 (러너가 로드) |

## 직접 구현한 부분

| 부분 | 위치 | 교체 후보 |
|---|---|---|
| 인메모리 프로젝트 저장 (`load_project`/`require_project`) | `app/runtime.py` | 영속 저장 필요 시 SQLite + SQLModel 등 |
