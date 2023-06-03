import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

PATH = "foodgram/data"


class Command(BaseCommand):
    help = "import data from ingredients.csv"

    def handle(self, *args, **options):
        with open(f'{PATH}/ingredients.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[0]
                # Здесь используется метод get_or_create() для избежания дубликатов
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully added ingredient "{name}"')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Ingredient "{name}" already exists')
                    )

