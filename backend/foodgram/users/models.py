from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'Логин',
        max_length=25,
        unique=True,
        help_text=('Логин должен быть 25 символов или меньше.'
                   'Только буквы, цифры и @/./+/-/_ '),
        validators=[username_validator],
        error_messages={
            'unique': "Пользователь с таким логином уже существует.",
        },
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Укажите имя'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Укажите фамилию',
        blank=False,
        null=False
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        help_text='Укажите электронную почту',
        blank=False,
        null=False,
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='following',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='follower',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='Пользователь не может подписаться сам на себя'
            ),
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='Подписаться на другого пользователя дважды запрещается'
            )
        ]
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
