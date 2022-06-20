import os
from pathlib import Path

from App.settings.jet_settings import *


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: str = Path(__file__).resolve().parent.parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# Applications definition
APP_NAME: str = "APPNAME"
URL: str = ""
FRONTEND_URL: str = ""

SPECIAL_APPS: list = [
    "jet.dashboard",
    "jet",
]  # Jet needs to charge before the admin app

DJANGO_APPS: list = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
]

THIRD_PARTY_APPS: list = [
    "django_rest_passwordreset",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_prometheus",
    "inline_static",
    "phonenumber_field",
]

LOCAL_APPS: list = ["App", "Users", "Emails"]

INSTALLED_APPS: list = (
    SPECIAL_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
)

AUTH_USER_MODEL: str = "Users.User"

MIDDLEWARE: list = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]


REST_FRAMEWORK: dict = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS: dict = {
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "TITLE": "Your Project API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/api/",
}


ROOT_URLCONF: str = "App.urls"

TEMPLATES: list = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "/App/App/static")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION: str = "App.wsgi.application"

CACHES: dict = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "redis:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

LOGGING: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/tmp/DjangoBackend.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE: str = "en-us"

TIME_ZONE: str = "UTC"

USE_I18N: bool = True

USE_TZ: bool = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL: str = "/static/"

MEDIA_DIRS: str = os.path.join(BASE_DIR, "/App/App/mMdia")
MEDIA_URL: str = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

# Celery params
CELERY_TIMEZONE: str = TIME_ZONE
CELERY_TASK_TRACK_STARTED: bool = True
CELERY_TASK_TIME_LIMIT: int = 30 * 60

# Suggestion email settings
SUGGESTIONS_EMAIL: str = ""
SUGGESTIONS_EMAIL_HEADER: str = "from user with id:"
EMAIL_GREETING: str = "Hi,"
SUGGESTIONS_EMAIL_LINK_TEXT: str = "Mark as read"

# Reset email settings
RESET_PASSWORD_EMAIL_SUBJECT: str = "Reset your password"
RESET_PASSWORD_EMAIL_HEADER: str = "Reset your password"
RESET_PASSWORD_EMAIL_LINK_TEXT: str = "Click here to reset your password"
RESET_PASSWORD_EMAIL_CONTENT: str = (
    "Click in the link below to change your password."
)
RESET_PASSWORD_EMAIL_LINK_TEXT: str = "Reset password"
RESET_PASSWORD_URL: str = (
    f""  # Must redirect a front url with the token in url
)

# Verify email settings
VERIFY_EMAIL_SUBJECT: str = "Verify your email"
VERIFY_EMAIL_HEADER: str = "Welcome to " + APP_NAME
VERIFY_EMAIL_LINK_TEXT: str = "Click here to reset your password"
VERIFY_EMAIL_CONTENT: str = (
    "First of all we want to thank you to give us a chance! "
    + "To fully start using the system and begin to be part "
    + "of the community, you must verify your email clicking"
    + "on the button below."
)
VERIFY_EMAIL_LINK_TEXT: str = "Verify email"
VERIFY_EMAIL_URL: str = f"{URL}/api/users"

# Storage

DEFAULT_FILE_STORAGE: str = "django.core.files.storage.FileSystemStorage"

AWS_ACCESS_KEY_ID: str = None
AWS_STORAGE_DOCUMENT_BUCKET_NAME: str = None
AWS_STORAGE_IMAGE_BUCKET_NAME: str = None
AWS_SECRET_ACCESS_KEY: str = None
AWS_S3_REGION_NAME: str = None
AWS_S3_SIGNATURE_VERSION: str = None
