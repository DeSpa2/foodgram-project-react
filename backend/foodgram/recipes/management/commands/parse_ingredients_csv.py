import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

PATH = "foodgram/data"


class Command(BaseCommand):
    help = "Импорт из ingredients.csv"

    def handle(self, *args, **options):
        with open(f'{PATH}/ingredients.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[0]
                measurement_unit = row[1]
                ingredient, created = Ingredient.objects.get_or_create(name=name, measurement_unit=measurement_unit)
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Ингредиент добавлен "{name}" с единицей измерения "{measurement_unit}"')
                    )
                elif name == 'пекарский порошок':
                    continue
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Ингредиент "{name}" с единицей измерения "{measurement_unit}" не добавлен')
                    )
