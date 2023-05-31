from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Наименование тега',
        max_length=200,
        unique=True,
        help_text='Укажите наименование тега'
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        null=True,
        unique=True,
        help_text='Укажите цвет тега'
    )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True,
        null=True,
        help_text='Укажите слаг тега'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Наименование ингредиента',
        max_length=200,
        unique=True,
        help_text='Укажите наименование ингредиента'
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        help_text='Укажите единицу измерения ингредиента'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент, связанный с рецептом'
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=(MinValueValidator(1),)
    )

    class Meta:
        verbose_name = 'Ингредиенты с количеством'
        verbose_name_plural = 'Ингредиенты с количеством'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'amount'),
                name='Связь ингредиента и его количества должна быть уникальна'
            )
        ]

    def __str__(self):
        return f'Ингредиент {self.ingredient} в количестве {self.amount}'


class Recipe(models.Model):
    name = models.CharField(
        'Наименование рецепта',
        max_length=200,
        help_text='Укажите наименование рецепта'
    )
    text = models.TextField(
        'Описание рецепта',
        help_text='Укажите описание рецепта'
    )
    image = models.ImageField(
        'Картинка рецепта',
        upload_to='recipes/images/',
        help_text='Добавьте картинку рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        IngredientRecipe,
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(1),),
        help_text='Укажите время приготовления рецепта (в минутах)'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Пользователь, добавляющий продукты в Избранное'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Рецепт, добавленный в Избранное'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='Запрещено добавлять рецепт дважды в Избранное'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в Избранное рецепт {self.recipe}'


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        related_name='baskets',
        on_delete=models.CASCADE,
        verbose_name='Пользователь, добавляющий рецепты в корзину'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='baskets',
        on_delete=models.CASCADE,
        verbose_name='Рецепты, добавленные в Корзину'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='Пользователь не может добавить рецепт в Корзину дважды'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в Корзину рецепт {self.recipe}'
