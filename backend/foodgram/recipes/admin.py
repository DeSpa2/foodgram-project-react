from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import (Ingredient, IngredientRecipe, Recipe, ShoppingCart, Tag,
                     TaggedRecipe)


class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)

    def count_favorites(self, obj):
        return obj.favorites.count()


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(TaggedRecipe)
admin.site.register(ShoppingCart)
admin.site.register(IngredientRecipe)
