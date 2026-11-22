from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.common.response import ApiResponse
from app.core.config.database import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> ApiResponse[dict]:
    return ApiResponse.ok({"status": "ok"})


@router.get("/db")
def health_db(db: Session = Depends(get_db)) -> ApiResponse[dict]:
    db.execute(text("SELECT 1"))
    postgis = db.execute(text("SELECT extversion FROM pg_extension WHERE extname = 'postgis'")).scalar()
    return ApiResponse.ok({"db": "ok", "postgis": postgis})
