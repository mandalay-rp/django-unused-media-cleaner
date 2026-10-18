import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "test-secret-key"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "unused_media_cleaner",
    "tests.testapp",
]

# Тестовое приложение не имеет миграций — таблицы создаются напрямую из моделей
MIGRATION_MODULES = {"testapp": None}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media_test")
MEDIA_URL = "/media/"

USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
