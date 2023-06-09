# Generated by Django 3.2.17 on 2023-05-30 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', to='recipes.IngredientRecipe', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингредиент, связанный с рецептом'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe', verbose_name='Рецепт, добавленный в Избранное'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, добавляющий продукты в Избранное'),
        ),
        migrations.AddField(
            model_name='basket',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baskets', to='recipes.recipe', verbose_name='Рецепты, добавленные в Корзину'),
        ),
        migrations.AddField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baskets', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, добавляющий рецепты в корзину'),
        ),
        migrations.AddConstraint(
            model_name='ingredientrecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'amount'), name='Связь ингредиента и его количества должна быть уникальна'),
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='Запрещено добавлять рецепт дважды в Избранное'),
        ),
        migrations.AddConstraint(
            model_name='basket',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='Пользователь не может добавить рецепт в Корзину дважды'),
        ),
    ]
