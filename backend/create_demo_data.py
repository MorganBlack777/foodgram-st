#!/usr/bin/env python3
import os
import sys
import django
from pathlib import Path
from django.core.files import File

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# Import models after Django setup
from django.contrib.auth import get_user_model  # noqa: E402
from recipe.models import Recipe, RecipeIngredient  # noqa: E402
from ingredient.models import Ingredient  # noqa: E402

User = get_user_model()

# Demo data
USERS = [
    {
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "avatar_file": "user1.png",
    },
    {
        "username": "user2",
        "email": "user2@example.com",
        "password": "password123",
        "first_name": "Jane",
        "last_name": "Smith",
        "avatar_file": "user2.png",
    },
    {
        "username": "user3",
        "email": "user3@example.com",
        "password": "password123",
        "first_name": "Alex",
        "last_name": "Johnson",
        "avatar_file": "user3.png",
    },
]

RECIPES = [
    {
        "name": "Блины",
        "text": "Классические русские блины. Тонкие, нежные и очень вкусные.",
        "cooking_time": 30,
        "image_file": "dish1.jpg",
        "author_username": "user1",
        "ingredients": [
            {"name_part": "мука", "amount": 200},
            {"name_part": "молоко", "amount": 500},
            {"name_part": "яйц", "amount": 3},
            {"name_part": "сахар", "amount": 30},
            {"name_part": "соль", "amount": 5},
            {"name_part": "масло", "amount": 30},
        ],
    },
    {
        "name": "Окрошка",
        "text": "Освежающий летний суп на квасе с овощами и мясом.",
        "cooking_time": 45,
        "image_file": "dish2.jpg",
        "author_username": "user2",
        "ingredients": [
            {"name_part": "квас", "amount": 1000},
            {"name_part": "огурц", "amount": 200},
            {"name_part": "карто", "amount": 300},
            {"name_part": "редис", "amount": 100},
            {"name_part": "колбас", "amount": 200},
            {"name_part": "яйц", "amount": 3},
            {"name_part": "зелен", "amount": 50},
            {"name_part": "сметан", "amount": 100},
        ],
    },
    {
        "name": "Борщ",
        "text": "Традиционный украинский борщ со свеклой, капустой и мясом.",
        "cooking_time": 120,
        "image_file": "dish3.jpg",
        "author_username": "user3",
        "ingredients": [
            {"name_part": "свекл", "amount": 300},
            {"name_part": "капуст", "amount": 200},
            {"name_part": "карто", "amount": 400},
            {"name_part": "морков", "amount": 100},
            {"name_part": "лук", "amount": 100},
            {"name_part": "говядин", "amount": 500},
            {"name_part": "томат", "amount": 100},
            {"name_part": "чеснок", "amount": 20},
            {"name_part": "соль", "amount": 10},
            {"name_part": "перец", "amount": 5},
            {"name_part": "лавр", "amount": 2},
        ],
    },
]


def find_ingredient_by_name_part(name_part):
    """Find an ingredient by partial name match."""
    return Ingredient.objects.filter(name__icontains=name_part).first()


def create_users():
    """Create demo users with avatars."""
    created_users = []

    for user_data in USERS:
        username = user_data["username"]

        # Skip if user already exists
        if User.objects.filter(username=username).exists():
            print(f"User {username} already exists, skipping...")
            continue

        # Create user
        user = User.objects.create_user(
            username=username,
            email=user_data["email"],
            password=user_data["password"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
        )

        # Add avatar if file exists
        avatar_path = Path(f"data/{user_data['avatar_file']}")
        if avatar_path.exists():
            with open(avatar_path, "rb") as f:
                user.avatar.save(user_data["avatar_file"], File(f), save=True)

        created_users.append(user)
        print(f"Created user: {user.username}")

    return created_users


def create_recipes():
    """Create demo recipes with images and ingredients."""
    created_recipes = []

    for recipe_data in RECIPES:
        name = recipe_data["name"]
        author_username = recipe_data["author_username"]

        # Skip if recipe already exists
        if Recipe.objects.filter(name=name).exists():
            print(f"Recipe {name} already exists, skipping...")
            continue

        # Get author
        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            print(
                f"Author {author_username} does not "
                f"exist, skipping recipe {name}..."
            )
            continue

        # Create recipe
        recipe = Recipe.objects.create(
            author=author,
            name=name,
            text=recipe_data["text"],
            cooking_time=recipe_data["cooking_time"],
        )

        # Add image if file exists
        image_path = Path(f"data/{recipe_data['image_file']}")
        if image_path.exists():
            with open(image_path, "rb") as f:
                recipe.image.save(
                    recipe_data["image_file"], File(f), save=True
                )

        # Add ingredients
        for ingredient_data in recipe_data["ingredients"]:
            ingredient = find_ingredient_by_name_part(
                ingredient_data["name_part"]
            )
            if ingredient:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=ingredient_data["amount"],
                )
            else:
                print(
                    f"Ingredient with name containing "
                    f"'{ingredient_data['name_part']}' not found"
                )

        created_recipes.append(recipe)
        print(f"Created recipe: {recipe.name}")

    return created_recipes


def main():
    print("Creating demo data...")

    # Check if ingredients exist
    if Ingredient.objects.count() == 0:
        print("No ingredients found. Please run load_ingredients.py first.")
        sys.exit(1)

    # Create users and recipes
    create_users()
    create_recipes()

    print("Demo data created successfully!")


if __name__ == "__main__":
    main()
