from django.db import models

from .constants import NAME_MAX_LENGTH, MEASUREMENT_UNIT_MAX_LENGTH


class Ingredient(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Ingredient's name",
        help_text="Ingredient's name",
    )
    measurement_unit = models.CharField(
        max_length=MEASUREMENT_UNIT_MAX_LENGTH,
        verbose_name="Measurement unit",
    )

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="unique_ingredient_unit_pair"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"
