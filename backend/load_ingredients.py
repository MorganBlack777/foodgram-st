#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django  # noqa: E402

django.setup()

from ingredient.models import Ingredient  # noqa: E402


def load_ingredients():
    """Load ingredients from JSON file into the database."""
    # Define the path to the ingredients file
    ingredients_path = Path("data/ingredients.json")

    # Check if file exists
    if not ingredients_path.exists():
        print(f"Error: Ingredients file not found at {ingredients_path}")
        sys.exit(1)

    try:
        # Open and load the JSON file
        with open(ingredients_path, encoding="utf-8") as f:
            ingredients_data = json.load(f)

        # Track statistics
        total_count = len(ingredients_data)
        created_count = 0
        existing_count = 0

        # Process each ingredient
        for item in ingredients_data:
            # Create the ingredient if it doesn't exist
            ingredient, created = Ingredient.objects.get_or_create(
                name=item["name"], measurement_unit=item["measurement_unit"]
            )

            if created:
                created_count += 1
            else:
                existing_count += 1

        # Print summary
        print("Ingredients loaded successfully:")
        print(f"  - Total ingredients in file: {total_count}")
        print(f"  - New ingredients created: {created_count}")
        print(f"  - Existing ingredients found: {existing_count}")

        return True

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {ingredients_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading ingredients: {e}")
        sys.exit(1)


if __name__ == "__main__":
    load_ingredients()
