from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Ni – AI Personal Operating System"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:///./data/ni.db"

    SECRET_KEY: str = "change-me-in-production-use-a-real-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    AI_PROVIDER: str = "mock"  # "openai" | "mock"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    CORS_ORIGINS: list[str] = ["*"]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
