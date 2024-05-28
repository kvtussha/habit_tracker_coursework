from django.db import models
from config.settings import AUTH_USER_MODEL
from habit.validators import OnlyOneFieldValidator, PleasantHabitValidator, NoRewardForPleasantHabitValidator, \
    FrequencyValidator, LastPerformedValidator
from django.core.validators import MinValueValidator, MaxValueValidator


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
    is_pleasant_habit = models.CharField(max_length=3, choices=BOOLEAN_CHOICES,
                                         verbose_name='Признак приятной привычки: Да или Нет')
    is_useful_habit = models.BooleanField(default=True, verbose_name='Признак полезной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE,
                                      verbose_name='Связанная привычка', default=None)
    frequency = models.IntegerField(default=1, verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=200, verbose_name='Вознаграждение')
    time_to_complete = models.IntegerField(verbose_name='Время на выполнение (в минутах)',
                                           validators=[MinValueValidator(1), MaxValueValidator(120)])
    is_public = models.CharField(max_length=3, choices=BOOLEAN_CHOICES,
                                 verbose_name='Признак публичности привычки: Да или Нет')

    def clean(self):
        OnlyOneFieldValidator()(self)
        PleasantHabitValidator()(self)
        NoRewardForPleasantHabitValidator()(self)
        FrequencyValidator()(self)
        LastPerformedValidator()(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
