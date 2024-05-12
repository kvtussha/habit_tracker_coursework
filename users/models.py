from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=100, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', null=True, blank=True)
    bot_id = models.BigIntegerField(verbose_name='Телеграмм id пользователя', unique=True)

    USERNAME_FIELD = 'bot_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
