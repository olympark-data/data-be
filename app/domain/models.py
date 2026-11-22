"""모든 도메인 모델을 한곳에서 import한다. Alembic(alembic/env.py)이 이 파일을 읽어 테이블을 찾는다.

새 도메인을 만들면 아래에 한 줄 추가:
    from app.domain.noise import models as noise_models  # noqa: F401
"""
