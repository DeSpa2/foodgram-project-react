from io import BytesIO

from django.db.models import Sum
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Basket, Favorites, Ingredient, IngredientRecipe,
                            Recipe, Tag)

from .filters import RecipeFilter
from .permissions import AuthorOrAdminOrReadOnly, IsAuthenticatedOrAdmin
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShortRecipeSerializer, TagSerializer)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        name = self.request.query_params['name'].lower()
        starts_with_queryset = list(
            self.queryset.filter(name__istartswith=name)
        )
        cont_queryset = self.queryset.filter(name__icontains=name)
        starts_with_queryset.extend(
            [x for x in cont_queryset if x not in starts_with_queryset]
        )
        return starts_with_queryset


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=(IsAuthenticatedOrAdmin,)
            )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = ShortRecipeSerializer(recipe)
            if Basket.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Данный рецепт уже есть в списке покупок'},
                    status=HTTP_400_BAD_REQUEST
                )
            Basket.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        if not Basket.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            return Response(
                {'errors': 'Данный рецепт в Корзине отсутствует'},
                status=HTTP_400_BAD_REQUEST
            )
        Basket.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=(IsAuthenticatedOrAdmin,)
            )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = ShortRecipeSerializer(recipe)
            if Favorites.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Данный рецепт уже добавлен в Избранное'},
                    status=HTTP_400_BAD_REQUEST
                )
            Favorites.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        if not Favorites.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            return Response(
                {'errors': 'Данный рецепт отсутствует в Избранном'},
                status=HTTP_400_BAD_REQUEST
            )
        Favorites.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrAdmin,)

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        request.data['recipe'] = recipe_id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        recipe_id = self.kwargs.get('recipe_id')
        shopping_cart_recipe_obj = Basket.objects.filter(
            user=self.request.user,
            recipe=recipe_id)
        return shopping_cart_recipe_obj


@api_view(['GET'])
def download_shopping_cart(request):
    user = request.user
    ingredients = (IngredientRecipe.objects
                   .filter(recipe__shopping_users=user)
                   .values('ingredient')
                   .annotate(sum_amount=Sum('amount'))
                   .values_list('ingredient__name',
                                'ingredient__measurement_unit',
                                'sum_amount'))

    file_buffer = BytesIO()
    pdf_canvas = canvas.Canvas(file_buffer, pagesize=letter)

    y_coordinate = 750

    for ingredient in ingredients:
        data_string = '{} {} - {}'.format(*ingredient)
        pdf_canvas.drawString(100, y_coordinate, data_string)
        y_coordinate -= 20

    pdf_canvas.save()

    file_buffer.seek(0)

    response = HttpResponse(
        file_buffer, content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="ingredients.pdf"')

    return response
