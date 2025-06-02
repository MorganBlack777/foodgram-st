"""
Конфигурационный файл Django проекта Foodgram.
Содержит все основные настройки приложения, включая базу данных,
статические файлы, аутентификацию и другие параметры.
"""

import hashlib
import os
from pathlib import Path

# Загрузка переменных окружения из .env файла при необходимости
if os.environ.get("DOTENV", False):
    from dotenv import load_dotenv

    load_dotenv()

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Настройки безопасности
# Секретный ключ генерируется автоматически, если не указан в переменных окружения
SECRET_KEY = os.environ.get(
    "SECRET_KEY", hashlib.sha256(os.urandom(24)).hexdigest()
)

# Режим отладки
DEBUG = os.environ.get("DEBUG", False)

# Разрешенные хосты
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "backend",
    os.environ.get("DOMAIN_NAME", "127.0.0.1"),
    os.environ.get("EXTERNAL_IP"),
    f"{os.environ.get('DOMAIN_NAME', '127.0.0.1')}:8080",
    f"{os.environ.get('EXTERNAL_IP')}:8080",
]

# Установленные приложения Django
INSTALLED_APPS = [
    # Стандартные приложения Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Сторонние библиотеки
    "rest_framework.authtoken",
    "rest_framework",
    "djoser",
    "django_filters",
    "drf_yasg",
    # Наши приложения
    "core.apps.CoreConfig",
    "ingredient.apps.IngredientConfig",
    "recipe.apps.RecipeConfig",
    "user.apps.UserConfig",
]

# Промежуточное ПО (middleware)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Конфигурация URL
ROOT_URLCONF = "backend.urls"

# Настройки шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Настройки WSGI
WSGI_APPLICATION = "backend.wsgi.application"

# Конфигурация баз данных
# В зависимости от настроек используется либо SQLite, либо PostgreSQL
if os.environ.get("USE_SQLITE", False) and os.environ.get("USE_SQLITE") != "0":
    # Конфигурация для SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # Конфигурация для PostgreSQL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "django"),
            "USER": os.getenv("POSTGRES_USER", "django"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", 5432),
            "OPTIONS": {"options": "-c search_path=foodgram_schema,public"},
        }
    }

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
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

# Настройки интернационализации
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# Настройки статических и медиа файлов
# Различаются для контейнеризированного и локального запуска
if os.environ.get("container", False):
    # Настройки для запуска в контейнере
    STATIC_URL = "/static_backend/"
    STATIC_ROOT = BASE_DIR / "static_backend"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = "/static/media"
else:
    # Настройки для локального запуска
    STATIC_URL = "/static_backend/"
    STATIC_ROOT = BASE_DIR / "static_backend"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = STATIC_ROOT / "media"

# Настройка автоматического поля ID для моделей
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Пользовательская модель
AUTH_USER_MODEL = "user.User"

# Настройки REST Framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "backend.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

# Настройки Djoser (для работы с пользователями API)
DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_ID_FIELD": "id",
    "HIDE_USERS": False,
    "SERIALIZERS": {
        "user": "user.serializers.CustomUserSerializer",
        "user_create": "user.serializers.CustomUserCreateSerializer",
        "current_user": "user.serializers.CustomUserSerializer",
    },
    "PERMISSIONS": {
        "user": ["rest_framework.permissions.IsAuthenticated"],
        "user_list": ["rest_framework.permissions.AllowAny"],
    },
}