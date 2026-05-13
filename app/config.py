from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///jobs.db"
    cors_origins: list[str] = ["*"]
    app_name: str = "Job Board"

    model_config = {"env_file": ".env"}


settings = Settings()
