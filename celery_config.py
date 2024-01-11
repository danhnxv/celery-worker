from celery import Celery
from app.config import CelerySettings
import os
from dotenv import load_dotenv

load_dotenv()

celery_settings = CelerySettings()

celery = Celery(
    "learning_celery",
    broker=celery_settings.broker_url,
)

celery.conf.timezone = os.getenv("CELERY_LOCAL_TIMEZONE")

celery.config_from_object(celery_settings)
