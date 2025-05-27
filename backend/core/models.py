from django.db import models

from .constants import SHORT_LINK_CODE_MAX_LENGTH
from recipe.models import Recipe
from user.models import User


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    subscribed_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "subscribed_to"], name="unique_subscription"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.username} subscribed to"
            f" {self.subscribed_to.username}"
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shopping_cart"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="in_shopping_carts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping_cart_recipe"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipe.name} in {self.user.username}'s shopping cart"


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite_recipe"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipe.name} favorited by {self.user.username}"


class ShortLink(models.Model):
    recipe = models.OneToOneField(
        Recipe, on_delete=models.CASCADE, related_name="short_link"
    )
    short_code = models.CharField(
        max_length=SHORT_LINK_CODE_MAX_LENGTH, unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Short link for {self.recipe.name}"
