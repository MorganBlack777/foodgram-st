import os
import random
from urllib.parse import urlunparse

from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .constants import SHORT_LINK_LETTERS, INGREDIENT_MIN_VALUE
from core.models import FavoriteRecipe, ShoppingCart, ShortLink
from ingredient.models import Ingredient
from user.serializers import CustomUserSerializer
from .models import Recipe, RecipeIngredient


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=INGREDIENT_MIN_VALUE)

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source="recipe_ingredients", many=True, read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(read_only=True, required=False)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False


        return request.user.favorite_recipes.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False

        return request.user.shopping_cart_items.filter(recipe=obj).exists()


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientForRecipeSerializer(many=True)
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ("ingredients", "name", "text", "cooking_time", "image")

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError(
                "Image field is required and cannot be empty."
            )
        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                "You need to add at least one ingredient."
            )

        ingredients_ids = [item["id"].id for item in value]
        if len(ingredients_ids) != len(set(ingredients_ids)):
            raise serializers.ValidationError("Ingredients must be unique.")

        return value

    @staticmethod
    def recipe_ingredients_by_data(recipe, ingredients_data):
        return [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_data["id"],
                amount=ingredient_data["amount"],
            )
            for ingredient_data in ingredients_data
        ]

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients", None)
        if ingredients_data is None or not ingredients_data:
            raise serializers.ValidationError(
                {
                    "ingredients": [
                        "This field is required and cannot be empty."
                    ]
                }
            )
        recipe = Recipe.objects.create(
            author=self.context["request"].user, **validated_data
        )

        recipe_ingredients = self.recipe_ingredients_by_data(
            recipe, ingredients_data
        )

        RecipeIngredient.objects.bulk_create(recipe_ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients", None)
        if ingredients_data is None or not ingredients_data:
            raise serializers.ValidationError(
                {
                    "ingredients": [
                        "This field is required and cannot be empty."
                    ]
                }
            )
        super().update(instance, validated_data)
        instance.save()

        instance.recipe_ingredients.all().delete()

        recipe_ingredients = self.recipe_ingredients_by_data(
            instance, ingredients_data
        )
        RecipeIngredient.objects.bulk_create(recipe_ingredients)
        return instance

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context=self.context).data


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class RecipeShortLinkSerializer(serializers.ModelSerializer):
    short_link = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("short-link",)

    @staticmethod
    def generate_short_link(recipe) -> ShortLink:
        code = "".join(random.choices(SHORT_LINK_LETTERS, k=6))
        return ShortLink.objects.create(recipe=recipe, short_code=code)

    def get_short_link(self, obj):
        request = self.context.get("request")
        host = (
            request.get_host()
            if request
            else os.environ.get("DOMAIN_NAME", "127.0.0.1")
        )
        protocol = "https" if request and request.is_secure() else "http"

        try:
            short_link = obj.short_link
        except ShortLink.DoesNotExist:
            short_link = self.generate_short_link(obj)

        return urlunparse((
            protocol,
            host,
            f"/s/{short_link.short_code}/",
            "",
            "",
            ""
        ))

    def to_representation(self, instance):
        return {"short-link": self.get_short_link(instance)}