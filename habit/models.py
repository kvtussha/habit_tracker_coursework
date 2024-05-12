from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {
    'blank': True,
    'null': True
}


class Habit(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                             null=True, blank=True)
    title = models.CharField(max_length=250, verbose_name='Название привычки', default='Название')
    place = models.CharField(max_length=250, verbose_name='Место выполнения привычки')
    time = models.TimeField(verbose_name='Время выполнения привычки')
    action = models.CharField(max_length=250, verbose_name='Действие привычки')
    is_pleasant_habit = models.BooleanField(verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE,
                                      verbose_name='Связанная привычка')
    frequency = models.IntegerField(default=1, verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=200, verbose_name='Вознаграждение')
    time_to_complete = models.IntegerField(verbose_name='Время на выполнение (в минутах)')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')
