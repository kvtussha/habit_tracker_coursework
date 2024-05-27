from django.db import models
from config.settings import AUTH_USER_MODEL

NULLABLE = {
    'blank': True,
    'null': True
}

class Habit(models.Model):
    YES = 'Да'
    NO = 'Нет'

    BOOLEAN_CHOICES = [
        (YES, 'Да'),
        (NO, 'Нет'),
    ]

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250, verbose_name='Название привычки', default='Название')
    place = models.CharField(max_length=250, verbose_name='Место выполнения привычки')
    time = models.TimeField(verbose_name='Время выполнения привычки')
    action = models.CharField(max_length=250, verbose_name='Действие привычки')
    is_pleasant_habit = models.CharField(max_length=3, choices=BOOLEAN_CHOICES, verbose_name='Признак приятной привычки: Да или Нет')
    is_useful_habit = models.BooleanField(default=True, verbose_name='Признак полезной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, verbose_name='Связанная привычка', default=None)
    frequency = models.IntegerField(default=1, verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=200, verbose_name='Вознаграждение')
    time_to_complete = models.IntegerField(verbose_name='Время на выполнение (в минутах)')
    is_public = models.CharField(max_length=3, choices=BOOLEAN_CHOICES, verbose_name='Признак публичности привычки: Да или Нет')

    def save(self, *args, **kwargs):
        if self.is_pleasant_habit == self.YES:
            self.is_useful_habit = False
            self.related_habit = None  # Приятная привычка не может иметь связанную привычку
        super().save(*args, **kwargs)
