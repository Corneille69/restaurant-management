from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Restaurant Management Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # PostgreSQL Backend Database
    DATABASE_URL: str = "postgresql+psycopg://restaurant_user:restaurant_password@restaurant-db:5432/restaurant_db"
    
    # Odoo Collaboration Configuration (Le patron pilote Odoo)
    ODOO_URL: str = "http://host.docker.internal:8070"
    ODOO_DB: str = "restaurant_odoo"
    ODOO_USER: str = "admin"
    ODOO_PASSWORD: str = "admin"

    # Sécurité et Authentification JWT
    SECRET_KEY: str = "secret-jwt-key-restaurant-patron-super-secure-change-in-prod-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 # 24 heures

    # Administrateur Initial par Défaut
    FIRST_ADMIN_USERNAME: str = "admin"
    FIRST_ADMIN_PASSWORD: str = "admin123"
    FIRST_ADMIN_EMAIL: str = "admin@restaurant.com"
    FIRST_ADMIN_FULL_NAME: str = "Administrateur Principal"
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
