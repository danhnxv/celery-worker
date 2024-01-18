from typing import Optional, Dict, List
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
import os
from celery.schedules import crontab


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="allow")
    # env variables
    LOG_LEVEL: str

    # mongodb
    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_DATABASE: str
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_EXPOSE_PORT: int

    SECRET_KEY: str
    ALGORITHM: str

    API_PORT: Optional[int]

    BACKEND_CORS_ORIGINS: List[str] = []

    ENVIRONMENT: str

    # Send mail
    MAIL_FROM: Optional[str]
    MAIL_PASSWORD: Optional[str]
    MAIL_PORT: Optional[str]
    MAIL_SERVER: Optional[str]


class CelerySettings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="allow")

    result_backend: Optional[str] = os.getenv("CELERY_RESUlT_BACKEND")
    mongodb_backend_settings: Dict[str, Optional[str]] = {
        "database": os.getenv("MONGODB_DATABASE"),
        "host": os.getenv("MONGODB_HOST"),
        "port": os.getenv("MONGODB_PORT"),
    }
    broker_url: Optional[str] = os.getenv("CELERY_BROKER_URL")
    include: List[str] = ["app.celery_tasks.send_email"]
    beat_schedule: Dict[str, dict] = {
        "send-reminder-email": {
            "task": "app.celery_tasks.send_email.send_reminder_order_email_task",
            "schedule": crontab(hour=0, minute=0),
        },
    }
    
settings = Settings()
