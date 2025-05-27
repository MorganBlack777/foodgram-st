"""
Конфигурация URL-маршрутов для проекта Foodgram.

Этот файл определяет все доступные URL-адреса API и административной панели,
а также настраивает документацию API с использованием Swagger и ReDoc.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from ingredient.views import IngredientViewSet
from recipe.views import RecipeViewSet
from user.views import CustomUserViewSet, UserAvatarView
from .views import health

# Создаем роутер Django REST Framework для автоматического создания URL-ов
маршрутизатор = DefaultRouter()

# Регистрируем ViewSet-ы в роутере
маршрутизатор.register("users", CustomUserViewSet, basename="users")
маршрутизатор.register("recipes", RecipeViewSet, basename="recipes")
маршрутизатор.register(
    "ingredients", IngredientViewSet, basename="ingredients"
)

# Настраиваем представление для документации Swagger/OpenAPI
документация_схемы = get_schema_view(
    openapi.Info(
        title="Foodgram - API для обмена рецептами",
        default_version="v1",
        description="API для проекта Foodgram - сервиса "
        "публикации и обмена кулинарными рецептами",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Список всех URL-маршрутов проекта
маршруты = [
    # Административная панель Django
    path("admin/", admin.site.urls),
    # API-эндпоинты
    path("api/", include(маршрутизатор.urls)),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("api/users/me/avatar/", UserAvatarView.as_view(), name="user-avatar"),
    # Эндпоинты для проверки работоспособности сервера
    path("api/health/", health, name="health-check"),
    # Документация API
    path(
        "swagger/",
        документация_схемы.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        документация_схемы.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(
        "api/docs/",
        документация_схемы.with_ui("redoc", cache_timeout=0),
        name="api-docs",
    ),
]

# Присваиваем маршруты переменной urlpatterns, которая используется Django
urlpatterns = маршруты

# Добавление обработчиков для медиа-файлов в режиме отладки
if settings.DEBUG:
    # Добавляем обработку URL-ов для медиа-файлов
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

    # Добавляем обработку URL-ов для статических файлов
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
