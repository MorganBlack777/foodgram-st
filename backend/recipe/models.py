from django.core.validators import MinValueValidator
from django.db import models

from .constants import MAX_RECIPE_NAME_LENGTH
from ingredient.models import Ingredient
from user.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    name = models.CharField(max_length=MAX_RECIPE_NAME_LENGTH)
    text = models.TextField()
    image = models.ImageField(upload_to="recipes/images/")
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message="Cooking time must be at least 1 minute"
            )
        ]
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="Amount must be at least 1")]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]

    def __str__(self):
        return (
            f"{self.ingredient.name} "
            f"({self.amount} {self.ingredient.measurement_unit})"
        )
