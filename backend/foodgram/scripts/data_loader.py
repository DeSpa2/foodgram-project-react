import csv

from recipes.models import Ingredient


def run():
    with open('scripts/ingredients.csv', encoding='Utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            Ingredient(name=row[0], measurement_unit=row[1]).save()
