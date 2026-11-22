# data-be

올림픽공원 프로젝트 백엔드. FastAPI + PostgreSQL(PostGIS), 도커로 실행해요.
프론트와 nginx는 data-fe 저장소에 있어요.

## 처음 실행

```bash
cp .env.example .env        # 값 채우기 (POSTGRES_PASSWORD와 DATABASE_URL의 비밀번호를 같게)
docker compose up -d --build
```

| 주소 | 내용 |
|---|---|
| http://localhost:8000/api/health | 백엔드 상태 |
| http://localhost:8000/api/health/db | DB, PostGIS 연결 확인 |
| localhost:5432 | 내 PC DB (내 PC DB 모드일 때만) |

## DB 선택 (내 PC DB / 공용 DB)

.env에서 두 묶음 중 하나만 켜면 돼요. 코드는 바꾸지 않아요.

| | 내 PC DB | 공용 DB |
|---|---|---|
| COMPOSE_PROFILES | local-db | (비움) |
| DATABASE_URL | db:5432 (도커로 같이 뜬 DB) | 공용 DB 주소 |
| RUN_MIGRATIONS | true | false |
| db 컨테이너 | 같이 뜸 | 안 뜸 |
| 마이그레이션 | 시작할 때 자동 적용 | 자동 적용 안 함 |

- 내 PC DB: 마음대로 테스트하고 지워도 되는 내 전용 DB예요. 새 마이그레이션은 여기서 먼저 확인해요.
- 공용 DB: 팀이 같이 보는 데이터예요. 내 브랜치의 마이그레이션이 들어가면 다른 팀원 DB가 깨지니까, 공용 DB에는 dev에 합쳐진 마이그레이션만 담당자가 적용해요.
  ```bash
  # dev 브랜치에서, 담당자만
  docker compose run --rm backend alembic upgrade head
  ```
- 모드를 바꾼 뒤에는 docker compose down 후 docker compose up -d로 다시 띄워요.

포트가 다른 프로젝트와 겹치면 .env의 DB_HOST_PORT, BACKEND_HOST_PORT를 바꾸세요.

app/ 폴더를 컨테이너에 연결해 두어서 코드를 저장하면 백엔드가 자동으로 다시 시작해요.

## 폴더 구조

```
data-be/
├── Dockerfile                   백엔드 이미지 빌드 (Python 3.12)
├── start.sh                     컨테이너 시작 (마이그레이션 → 서버 실행)
├── .dockerignore                이미지에 넣지 않을 파일
├── docker-compose.yml           로컬 실행 (db, backend)
├── requirements.txt             패키지 버전 고정
├── .env.example                 환경 변수 예시 (.env는 커밋 금지)
├── alembic.ini
├── alembic/versions/            마이그레이션 (Flyway 대체)
├── app/
│   ├── main.py                  앱 생성, 라우터 등록
│   ├── domain/                  비즈니스 로직
│   │   ├── models.py            모든 도메인 모델 등록 (Alembic용)
│   │   └── {도메인}/            dto.py, models.py, repository.py, service.py, client.py
│   ├── core/                    공통 (Spring global 대체)
│   │   ├── common/              Base, TimestampMixin, ApiResponse, PageResponse
│   │   ├── config/              settings, database(get_db), cors
│   │   ├── error/               AppException, 전역 예외 핸들러
│   │   └── util/
│   ├── web/                     HTTP 입구
│   │   └── {도메인}/            router.py, dto/request.py, dto/response.py
│   └── analysis/                분석·예측 모델 (artifacts/는 커밋 금지)
└── tests/                       web/, domain/, integration/
```

## 새 도메인 추가 순서

예: noise

1. app/domain/noise/에 __init__.py, models.py, dto.py, repository.py, service.py를 만들어요.
2. app/domain/models.py에 한 줄 추가해요. 빠뜨리면 Alembic이 테이블을 못 찾아요.
   ```python
   from app.domain.noise import models as noise_models  # noqa: F401
   ```
3. app/web/noise/에 __init__.py, router.py, dto/__init__.py, dto/request.py, dto/response.py를 만들어요.
4. app/main.py에 api.include_router(noise_router)를 추가해요.
5. 마이그레이션을 만들고 적용해요.
   ```bash
   docker compose exec backend alembic revision --autogenerate -m "create noise tables"
   # alembic/versions/에 생긴 파일을 열어서 확인
   docker compose exec backend alembic upgrade head
   ```

## 마이그레이션 주의

- 내 PC DB 모드에서는 컨테이너가 시작할 때 alembic upgrade head가 자동으로 실행돼요. 공용 DB 모드에서는 실행되지 않아요.
- 컬럼 이름 변경은 autogenerate가 "삭제 후 추가"로 만들어요. 데이터가 사라지니 생성된 파일을 꼭 확인하고 op.alter_column으로 고치세요.
- 우리 모델에 없는 테이블(PostGIS가 만드는 tiger, topology 테이블)은 비교에서 빼 두었어요. 그래서 모델을 지워도 drop_table은 자동으로 생기지 않아요. 테이블을 지울 때는 마이그레이션에 직접 적어요.

## 테스트

```bash
docker compose exec backend pytest -q
```

## 환경별 차이

코드는 같고 .env만 달라요.

| 값 | 로컬 | 온프레미스 (Rocky VM, 테스트) | EC2 (운영) |
|---|---|---|---|
| DATABASE_URL | db:5432 | DB VM 주소 | DB 인스턴스 또는 RDS 주소 |
| CORS_ORIGINS | localhost | 테스트 서버 도메인 | 운영 도메인 |
