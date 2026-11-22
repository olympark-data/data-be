from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """환경마다 달라지는 값. 로컬·온프레미스·EC2는 .env만 다르게 둔다."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"
    database_url: str
    cors_origins: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
