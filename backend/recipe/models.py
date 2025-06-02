from django.core.validators import MinValueValidator
from django.db import models

from ingredient.models import Ingredient
from user.models import User
from .constants import (
    NAME_MAX_LENGTH,
    TEXT_MAX_LENGTH,
    MIN_COOKING_TIME,
    MIN_AMOUNT
)


class Tag(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        verbose_name="Tag name"
    )
    slug = models.SlugField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        verbose_name="Tag slug"
    )
    color = models.CharField(
        max_length=7,
        verbose_name="Color in HEX format"
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Recipe name"
    )
    text = models.TextField(
        max_length=TEXT_MAX_LENGTH,
        verbose_name="Recipe description"
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_COOKING_TIME)],
        verbose_name="Cooking time in minutes"
    )
    image = models.ImageField(
        upload_to="recipes/",
        verbose_name="Recipe image"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Recipe author"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        verbose_name="Recipe tags"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients"
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_AMOUNT)],
        verbose_name="Amount"
    )

    class Meta:
        verbose_name = "Recipe ingredient"
        verbose_name_plural = "Recipe ingredients"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient"
            )
        ]
    def __str__(self):
        return f"{self.ingredient.name} in {self.recipe.name}"

class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shopping_cart"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="in_shopping_carts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Shopping cart item"
        verbose_name_plural = "Shopping cart items"
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
        verbose_name = "Favorite recipe"
        verbose_name_plural = "Favorite recipes"
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
        max_length=10, unique=True  # импортировать константу из core.constants
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Short link"
        verbose_name_plural = "Short links"

    def __str__(self):
        return f"Short link for {self.recipe.name}"