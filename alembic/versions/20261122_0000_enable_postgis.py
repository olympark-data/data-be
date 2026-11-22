"""enable postgis

로컬 postgis 이미지는 자동으로 켜 주지만, RDS 등 다른 환경에서도 같은 상태가 되도록 마이그레이션으로 남긴다.

Revision ID: 0001_enable_postgis
Revises:
Create Date: 2026-11-22
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0001_enable_postgis"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS postgis")
