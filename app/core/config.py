from pydantic_settings import BaseSettings
from typing import List
import secrets
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Document Management System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "newuser"
    POSTGRES_PASSWORD: str = "StrongPass123"
    POSTGRES_DB: str = "newdb"
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    
    # CORS
    CORS_ALLOWED_ORIGINS: str = "http://localhost:4200,http://127.0.0.1:4200"
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",")]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 