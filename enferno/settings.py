# -*- coding: utf-8 -*-
import os
from datetime import timedelta

import bleach
import redis
from dotenv import load_dotenv, find_dotenv

from enferno.utils.config_utils import ConfigManager

load_dotenv(find_dotenv())
manager = ConfigManager()


def uia_username_mapper(identity):
    # we allow pretty much anything - but we bleach it.
    return bleach.clean(identity, strip=True)


class Config(object):
    BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000/")

    SECRET_KEY = os.environ.get("SECRET_KEY")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_ENABLED = os.environ.get("DEBUG_TB_ENABLED", 0)
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "redis"  # Can be "memcached", "redis", etc.

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    # Databaset
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "bayanat")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

    if (POSTGRES_USER and POSTGRES_PASSWORD) or POSTGRES_HOST != "localhost":
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql:///{POSTGRES_DB}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"

    # Celery
    # Has to be in small case
    celery_broker_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2"
    result_backend = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/3"

    # Security
    SECURITY_REGISTERABLE = manager.get_config("SECURITY_REGISTERABLE")
    SECURITY_RECOVERABLE = manager.get_config("SECURITY_RECOVERABLE")
    SECURITY_CONFIRMABLE = manager.get_config("SECURITY_CONFIRMABLE")
    SECURITY_CHANGEABLE = True
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_POST_LOGIN_VIEW = "/dashboard/"
    SECURITY_POST_CONFIRM_VIEW = "/dashboard/"

    SECURITY_USER_IDENTITY_ATTRIBUTES = [
        {"username": {"mapper": uia_username_mapper, "case_insensitive": True}}
    ]
    SECURITY_USERNAME_ENABLE = True

    SECURITY_MULTI_FACTOR_RECOVERY_CODES = True
    SECURITY_MULTI_FACTOR_RECOVERY_CODES_N = 3
    SECURITY_MULTI_FACTOR_RECOVERY_CODES_KEYS = None
    SECURITY_MULTI_FACTOR_RECOVERY_CODE_TTL = None

    # Disable token apis

    SECURITY_TWO_FACTOR_ENABLED_METHODS = [
        "authenticator"
    ]  # 'sms' also valid but requires an sms provider
    SECURITY_TWO_FACTOR = os.environ.get("SECURITY_TWO_FACTOR")
    SECURITY_TWO_FACTOR_RESCUE_MAIL = os.environ.get("SECURITY_TWO_FACTOR_RESCUE_MAIL")

    # Enable only session auth
    SECURITY_API_ENABLED_METHODS = ["session"]
    security_freshness = manager.get_config("SECURITY_FRESHNESS")
    SECURITY_FRESHNESS = timedelta(minutes=security_freshness)

    security_freshness_grace_period = manager.get_config("SECURITY_FRESHNESS_GRACE_PERIOD")
    SECURITY_FRESHNESS_GRACE_PERIOD = timedelta(minutes=security_freshness_grace_period)

    SECURITY_TWO_FACTOR_REQUIRED = manager.get_config("SECURITY_TWO_FACTOR_REQUIRED")

    SECURITY_PASSWORD_LENGTH_MIN = manager.get_config("SECURITY_PASSWORD_LENGTH_MIN")

    SECURITY_PASSWORD_COMPLEXITY_CHECKER = "zxcvbn"

    SECURITY_ZXCVBN_MINIMUM_SCORE = manager.get_config("SECURITY_ZXCVBN_MINIMUM_SCORE")

    # Strong session protection
    SESSION_PROTECTION = "strong"

    # 2fa
    SECURITY_TOTP_SECRETS = {"1": os.environ.get("SECURITY_TOTP_SECRETS")}
    SECURITY_TOTP_ISSUER = "Bayanat"

    SECURITY_WEBAUTHN = manager.get_config("SECURITY_WEBAUTHN")
    SECURITY_WAN_ALLOW_AS_FIRST_FACTOR = False
    SECURITY_WAN_ALLOW_AS_MULTI_FACTOR = True
    SECURITY_WAN_ALLOW_AS_VERIFY = ["first", "secondary"]
    SECURITY_WAN_ALLOW_USER_HINTS = True

    # Recaptcha
    RECAPTCHA_ENABLED = manager.get_config("RECAPTCHA_ENABLED")
    RECAPTCHA_PUBLIC_KEY = manager.get_config("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = manager.get_config("RECAPTCHA_PRIVATE_KEY")

    # Session
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url(f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/1")
    PERMANENT_SESSION_LIFETIME = 3600

    # Google 0Auth
    GOOGLE_OAUTH_ENABLED = manager.get_config("GOOGLE_OAUTH_ENABLED")
    GOOGLE_CLIENT_ID = manager.get_config("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = manager.get_config("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = manager.get_config("GOOGLE_DISCOVERY_URL")

    GOOGLE_CLIENT_ALLOWED_DOMAIN = os.environ.get("GOOGLE_CLIENT_ALLOWED_DOMAIN", False)

    # File Upload Settings: switch to True to store files privately within the enferno/media directory
    FILESYSTEM_LOCAL = manager.get_config("FILESYSTEM_LOCAL")

    # Access Control settings
    ACCESS_CONTROL_RESTRICTIVE = manager.get_config("ACCESS_CONTROL_RESTRICTIVE")

    # Activities
    ACTIVITIES = manager.get_config("ACTIVITIES")
    activities = [x for x, value in ACTIVITIES.items() if value]
    # minimum retention for 90 days
    activities_retention = max(90, int(manager.get_config("ACTIVITIES_RETENTION")))
    ACTIVITIES_RETENTION = timedelta(days=activities_retention)

    # Allowed file upload extensions
    MEDIA_ALLOWED_EXTENSIONS = manager.get_config("MEDIA_ALLOWED_EXTENSIONS")
    MEDIA_UPLOAD_MAX_FILE_SIZE = manager.get_config("MEDIA_UPLOAD_MAX_FILE_SIZE")
    SHEETS_ALLOWED_EXTENSIONS = manager.get_config("SHEETS_ALLOWED_EXTENSIONS")

    # Enable data import tool
    ETL_TOOL = manager.get_config("ETL_TOOL")
    ETL_PATH_IMPORT = manager.get_config("ETL_PATH_IMPORT")
    ETL_ALLOWED_PATH = os.environ.get("ETL_ALLOWED_PATH", None)

    EXPORT_TOOL = manager.get_config("EXPORT_TOOL")
    # Export file expiry in hours
    export_default_expiry = manager.get_config("EXPORT_DEFAULT_EXPIRY")
    EXPORT_DEFAULT_EXPIRY = timedelta(hours=export_default_expiry)

    # Enable data deduplication tool
    DEDUP_TOOL = manager.get_config("DEDUP_TOOL")

    # Valid video extension list (will be processed during ETL)
    ETL_VID_EXT = manager.get_config("ETL_VID_EXT")

    # valid image extenstions supported by Tesseract OCR
    OCR_ENABLED = manager.get_config("OCR_ENABLED")
    OCR_EXT = manager.get_config("OCR_EXT")
    TESSERACT_CMD = os.environ.get("TESSERACT_CMD", "/usr/bin/tesseract")

    # S3 settings
    # Bucket needs to be private with public access blocked
    AWS_ACCESS_KEY_ID = manager.get_config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = manager.get_config("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET = manager.get_config("S3_BUCKET")
    AWS_REGION = manager.get_config("AWS_REGION")

    # i18n
    LANGUAGES = ["en", "ar", "uk", "fr", "es", "ru", "fa"]
    BABEL_DEFAULT_LOCALE = manager.get_config("BABEL_DEFAULT_LOCALE")
    # extract messages with the following command
    # pybabel extract -F babel.cfg -k _l -o messages.pot .
    # generate a new language using the following command
    # pybabel init -i messages.pot -d enferno/translations -l ar
    # to update existing translations
    # pybabel update -i messages.pot -d enferno/translations
    # compile translation using the following
    # pybabel compile -d enferno/translations

    MAPS_API_ENDPOINT = manager.get_config("MAPS_API_ENDPOINT")
    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

    # Deduplication

    # specify min and max distance for matching
    DEDUP_LOW_DISTANCE = manager.get_config("DEDUP_LOW_DISTANCE")
    DEDUP_MAX_DISTANCE = manager.get_config("DEDUP_MAX_DISTANCE")

    # how many items to process every cycle (cycles are processed based on the time interval below)
    DEDUP_BATCH_SIZE = manager.get_config("DEDUP_BATCH_SIZE")

    # the time in seconds at which a batch of deduplication items is processed
    DEDUP_INTERVAL = manager.get_config("DEDUP_INTERVAL")

    # Sheet import tool settings
    SHEET_IMPORT = manager.get_config("SHEET_IMPORT")
    IMPORT_DIR = "enferno/imports"

    geo_map_default_center = manager.get_config("GEO_MAP_DEFAULT_CENTER")

    if geo_map_default_center:
        GEO_MAP_DEFAULT_CENTER_LAT = geo_map_default_center.get("lat")
        GEO_MAP_DEFAULT_CENTER_LNG = geo_map_default_center.get("lng")

    ITEMS_PER_PAGE_OPTIONS = manager.get_config("ITEMS_PER_PAGE_OPTIONS")
    VIDEO_RATES = manager.get_config("VIDEO_RATES")
    # secure cookies (flask core)
    SESSION_COOKIE_SECURE = os.environ.get("SECURE_COOKIES", "True") == "True"
    REMEMBER_COOKIE_SECURE = os.environ.get("SECURE_COOKIES", "True") == "True"
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # flask-security cookie
    SECURITY_CSRF_COOKIE = {
        # Overrides default secure = False to require HTTPS.
        "samesite": "Strict",
        "httponly": False,
        "secure": os.environ.get("SECURE_COOKIES", "True") == "True",
    }


class TestConfig(Config):
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    if (POSTGRES_USER and POSTGRES_PASSWORD) or POSTGRES_HOST != "localhost":
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/bayanat_test"
        )
    else:
        SQLALCHEMY_DATABASE_URI = "postgresql:///bayanat_test"
    # Redis
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/15"
    # Celery
    # Has to be in small case
    celery_broker_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/14"
    result_backend = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/13"
    SESSION_REDIS = redis.from_url(f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/12")
