from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from api.permissions import IsAuthenticatedOrAdmin

from .models import Follow
from .serializers import CustomUserSerializer, FollowSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticatedOrAdmin,))
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(page,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=(IsAuthenticatedOrAdmin,)
            )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if user.id == author.id:
                return Response({'detail': 'Нельзя подписаться на себя'},
                                status=status.HTTP_400_BAD_REQUEST)
            if Follow.objects.filter(author=author, user=user).exists():
                return Response({'detail': 'Вы уже подписаны!'},
                                status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(author,
                                          context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Follow.objects.filter(user=user, author=author).exists():
                return Response({'errors': 'Вы не подписаны'},
                                status=status.HTTP_400_BAD_REQUEST)
            subscription = get_object_or_404(Follow,
                                             user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


    @subscribe.mapping.delete
    def delete_subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        if not Follow.objects.filter(
                user=request.user,
                author=author
        ).exists():
            return Response(
                {'errors': 'Данная подписка не существует'},
                status=HTTP_400_BAD_REQUEST
            )
        Follow.objects.filter(
            user=request.user,
            author=author
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)
