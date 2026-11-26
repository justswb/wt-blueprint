# wt-blueprint
## 런타임·패키지

| 이름 | 버전 | 용도 | 라이선스 |
|---|---|---|---|
| Python | 3.15 (`requires-python >=3.15`) | 런타임 | PSF-2.0 |
| uv | 0.13.6 | 의존성 설치·실행 | Apache-2.0 |
| fastapi[standard] | 0.165.0 | API 서버 | MIT |
| pydantic | 2.14.4 | 데이터 모델 검증 (fastapi 의존성) | MIT |
| httpx | 0.28.1 | `TestClient` 백엔드 | BSD-3-Clause |
| pytest | 9.2.0 | 테스트 | MIT |

Python 패키지 버전은 `uv.lock`으로 고정된다.

```sh
uv sync          # 의존성 설치 (.venv)
uv run pytest    # 테스트
```

uv는 전역 설치가 필요하다: https://docs.astral.sh/uv/
