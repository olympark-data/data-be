from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

import app.domain.models  # noqa: F401  모든 도메인 모델을 불러와야 autogenerate가 테이블을 찾아요
from alembic import context
from app.core.common.base import Base
from app.core.config.settings import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# 우리 모델(Base.metadata)에 없는 DB 테이블은 비교 대상에서 뺀다.
# 공용 DB에 다른 용도의 테이블이 있어도 autogenerate가 삭제하려 하지 않게 하기 위해서다.
# 대신 모델을 지워도 drop_table은 자동으로 안 생기니, 테이블 삭제는 마이그레이션에 직접 적는다.
def include_object(obj, name, type_, reflected, compare_to):
    if type_ == "table" and reflected and compare_to is None:
        return False
    if type_ in ("index", "column", "unique_constraint", "foreign_key_constraint") and reflected and compare_to is None:
        table = getattr(obj, "table", None)
        if table is not None and table.name not in target_metadata.tables:
            return False
    return True


def run_migrations_offline() -> None:
    context.configure(url=settings.database_url, target_metadata=target_metadata,
                      literal_binds=True, include_object=include_object)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}),
                                     prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata,
                          include_object=include_object, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
