from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Inventory System"
    SECRET_KEY: str = "very-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "postgresql://user:pass@localhost/dbname"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()