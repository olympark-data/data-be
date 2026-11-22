#!/bin/sh
# 컨테이너 시작 스크립트
# RUN_MIGRATIONS=false 이면 마이그레이션을 건너뛴다 (공용 DB를 쓸 때)
set -e
if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  alembic upgrade head
else
  echo "RUN_MIGRATIONS=false: 마이그레이션을 건너뜁니다"
fi
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 "$@"
