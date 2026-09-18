import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Must happen before the Config class body below reads os.environ — class attributes are
# evaluated once, at class-definition time, so .env has to be loaded before this point or
# every value silently falls back to its default.
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-before-deploying")

    MONGO_URI = os.environ.get("MONGO_URI", "")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "jennie_hairport")

    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "jennie-admin-2026")

    SQUAD_SECRET_KEY = os.environ.get("SQUAD_SECRET_KEY", "")
    SQUAD_PUBLIC_KEY = os.environ.get("SQUAD_PUBLIC_KEY", "")
    SQUAD_ENV = os.environ.get("SQUAD_ENV", "sandbox")

    SITE_BASE_URL = os.environ.get("SITE_BASE_URL", "http://localhost:5000")

    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8MB upload limit
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
