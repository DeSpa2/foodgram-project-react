from io import BytesIO

from django.db.models import Sum
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet

from recipes.models import Basket, IngredientRecipe

from .permissions import IsAuthenticatedOrAdmin
from .serializers import RecipeSerializer


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
