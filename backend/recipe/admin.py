from django.contrib import admin
from django.db.models import Count

from .models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1
    autocomplete_fields = ("ingredient",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "cooking_time", "get_favorites_count")
    search_fields = ("name", "author__username", "author__email")
    list_filter = ("author", "cooking_time")
    readonly_fields = ("get_favorites_count",)
    inlines = (RecipeIngredientInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(favorites_count=Count("favorited_by"))
        return queryset

    def get_favorites_count(self, obj):
        return obj.favorites_count

    get_favorites_count.short_description = "Favorites"
    get_favorites_count.admin_order_field = "favorites_count"


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount")
    search_fields = ("recipe__name", "ingredient__name")
    autocomplete_fields = ("recipe", "ingredient")
