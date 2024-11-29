import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    #App Configuration
    PROJECT_NAME: str = "Referral System"
    API_PREFIX: str = "/api/v1"
    
    #Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    #Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")
    PYTHON_ENVIRONMENT: str = os.getenv("PYTHON_ENVIRONMENT")
    ALGORITHM = "HS256"
    REFRESH_TOKEN_EXPIRE_MINUTES = 90
    ACCESS_TOKEN_EXPIRE_MINUTES = 15

    #SMTP Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587)) 
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    SMTP_SENDER_EMAIL: str = os.getenv("SENDER_EMAIL")
    SMTP_FROM_NAME: str = os.getenv("SMTP_FROM_NAME")

settings = Settings()