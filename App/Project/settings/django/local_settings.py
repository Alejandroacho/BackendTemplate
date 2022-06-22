from datetime import timedelta

from Project.settings.django.default_settings import *


URL: str = "http://localhost:8000"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = "default-secret-key"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = True
ENVIRONMENT_NAME: str = "dev"
ALLOWED_HOSTS: list = []


STATICFILES_DIRS: tuple = (os.path.join(BASE_DIR, "/App/Project/static"),)
STATIC_ROOT: str = os.path.join(BASE_DIR, "staticfiles")

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES: dict = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "databasename",
        "USER": "root",
        "PASSWORD": "password",
        "HOST": "database",  # <-- docker host name for db
        "PORT": "3306",  # <-- docker port for db
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "sql_mode": "STRICT_TRANS_TABLES",
        },
        "TEST": {
            # https://docs.djangoproject.com/en/4.0/topics/testing/overview/#the-test-database
            "NAME": "test_database"
        },
    }
}

# TOKEN TO VERIFY USER VIA EMAIL
EMAIL_VERIFICATION_TOKEN_SECRET: str = "hu712dkej_803h7719)a4n-5!5n0cr((2l"

# SMTP CONFIG
EMAIL_HOST: str = ""
EMAIL_HOST_USER: str = ""
EMAIL_HOST_PASSWORD: str = ""
EMAIL_PORT: str = ""

# Email settings
TEST_EMAIL: str = "test@ing.email"
SUGGESTIONS_EMAIL: str = "test@suggestion.email"

# Verify email settings
VERIFY_EMAIL_URL: str = f"{URL}/api/users"

SIMPLE_JWT: dict = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=100),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}
