from fastapi import APIRouter, FastAPI

from app.core.config.cors import add_cors
from app.core.error.handlers import register_exception_handlers
from app.web.health.router import router as health_router


def create_app() -> FastAPI:
    # Swagger(문서 화면)는 쓰지 않아서 문서 관련 주소를 모두 끈다
    app = FastAPI(title="olympicpark API", docs_url=None, redoc_url=None, openapi_url=None)
    add_cors(app)
    register_exception_handlers(app)

    api = APIRouter(prefix="/api")
    api.include_router(health_router)
    # 새 도메인 라우터는 여기에 추가: api.include_router(noise_router)
    app.include_router(api)
    return app


app = create_app()
