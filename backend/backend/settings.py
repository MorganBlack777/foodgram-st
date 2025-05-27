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
КОРНЕВАЯ_ДИРЕКТОРИЯ = Path(__file__).resolve().parent.parent

# Настройки безопасности
# Секретный ключ генерируется автоматически, если не указан в переменных окружения
СЕКРЕТНЫЙ_КЛЮЧ = os.environ.get(
    "SECRET_KEY", hashlib.sha256(os.urandom(24)).hexdigest()
)
SECRET_KEY = СЕКРЕТНЫЙ_КЛЮЧ

# Режим отладки
РЕЖИМ_ОТЛАДКИ = os.environ.get("DEBUG", False)
DEBUG = РЕЖИМ_ОТЛАДКИ

# Разрешенные хосты
РАЗРЕШЕННЫЕ_ХОСТЫ = [
    "127.0.0.1",
    "localhost",
    "backend",
    os.environ.get("DOMAIN_NAME", "127.0.0.1"),
    os.environ.get("EXTERNAL_IP"),
    f"{os.environ.get('DOMAIN_NAME', '127.0.0.1')}:8080",
    f"{os.environ.get('EXTERNAL_IP')}:8080",
]
ALLOWED_HOSTS = РАЗРЕШЕННЫЕ_ХОСТЫ

# Установленные приложения Django
УСТАНОВЛЕННЫЕ_ПРИЛОЖЕНИЯ = [
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
INSTALLED_APPS = УСТАНОВЛЕННЫЕ_ПРИЛОЖЕНИЯ

# Промежуточное ПО (middleware)
ПРОМЕЖУТОЧНОЕ_ПО = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
MIDDLEWARE = ПРОМЕЖУТОЧНОЕ_ПО

# Конфигурация URL
КОРНЕВОЙ_URLCONF = "backend.urls"
ROOT_URLCONF = КОРНЕВОЙ_URLCONF

# Настройки шаблонов
ШАБЛОНЫ = [
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
TEMPLATES = ШАБЛОНЫ

# Настройки WSGI
WSGI_ПРИЛОЖЕНИЕ = "backend.wsgi.application"
WSGI_APPLICATION = WSGI_ПРИЛОЖЕНИЕ

# Конфигурация баз данных
# В зависимости от настроек используется либо SQLite, либо PostgreSQL
if os.environ.get("USE_SQLITE", False) and os.environ.get("USE_SQLITE") != "0":
    # Конфигурация для SQLite
    БАЗЫ_ДАННЫХ = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": КОРНЕВАЯ_ДИРЕКТОРИЯ / "db.sqlite3",
        }
    }
else:
    # Конфигурация для PostgreSQL
    БАЗЫ_ДАННЫХ = {
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
DATABASES = БАЗЫ_ДАННЫХ

# Валидаторы паролей
ВАЛИДАТОРЫ_ПАРОЛЕЙ = [
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
AUTH_PASSWORD_VALIDATORS = ВАЛИДАТОРЫ_ПАРОЛЕЙ

# Настройки интернационализации
КОД_ЯЗЫКА = "ru-ru"
LANGUAGE_CODE = КОД_ЯЗЫКА

ЧАСОВОЙ_ПОЯС = "Europe/Moscow"
TIME_ZONE = ЧАСОВОЙ_ПОЯС

USE_I18N = True
USE_TZ = True

# Настройки статических и медиа файлов
# Различаются для контейнеризированного и локального запуска
if os.environ.get("container", False):
    # Настройки для запуска в контейнере
    STATIC_URL = "/static_backend/"
    STATIC_ROOT = КОРНЕВАЯ_ДИРЕКТОРИЯ / "static_backend"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = "/static/media"
else:
    # Настройки для локального запуска
    STATIC_URL = "/static_backend/"
    STATIC_ROOT = КОРНЕВАЯ_ДИРЕКТОРИЯ / "static_backend"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = STATIC_ROOT / "media"

# Настройка автоматического поля ID для моделей
ПОЛЕ_АВТО_ID = "django.db.models.BigAutoField"
DEFAULT_AUTO_FIELD = ПОЛЕ_АВТО_ID

# Пользовательская модель
МОДЕЛЬ_ПОЛЬЗОВАТЕЛЯ = "user.User"
AUTH_USER_MODEL = МОДЕЛЬ_ПОЛЬЗОВАТЕЛЯ

# Настройки REST Framework
REST_FRAMEWORK_НАСТРОЙКИ = {
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
REST_FRAMEWORK = REST_FRAMEWORK_НАСТРОЙКИ

# Настройки Djoser (для работы с пользователями API)
DJOSER_НАСТРОЙКИ = {
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
DJOSER = DJOSER_НАСТРОЙКИ
