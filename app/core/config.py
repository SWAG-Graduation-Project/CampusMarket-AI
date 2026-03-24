from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "CampusMarket AI"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    ALLOWED_ORIGINS: list[str] = ["*"]

    GEMINI_API_KEY: str = ""

    MAX_UPLOAD_IMAGES: int = 5
    MAX_IMAGE_SIZE_MB: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
