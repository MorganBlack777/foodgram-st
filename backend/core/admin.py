from django.contrib import admin

from .models import FavoriteRecipe, ShoppingCart, ShortLink, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "subscribed_to", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "subscribed_to__username",
        "subscribed_to__email",
    )
    list_filter = ("created_at",)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe", "created_at")
    search_fields = ("user__username", "user__email", "recipe__name")
    list_filter = ("created_at",)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe", "created_at")
    search_fields = ("user__username", "user__email", "recipe__name")
    list_filter = ("created_at",)


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ("recipe", "short_code", "created_at")
    search_fields = ("recipe__name", "short_code")
    list_filter = ("created_at",)
