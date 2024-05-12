from django.core.exceptions import ValidationError
from django.utils import timezone


class HabitValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # Проверка на заполнение только одного из полей reward и related_habit
        if self.field == 'reward':
            if value and getattr(self.instance, 'related_habit', None):
                raise ValidationError(
                    "Только одно из полей 'вознаграждение' и 'связанная привычка' может быть заполнено.")

        # Проверка на связанную привычку только для приятных привычек
        elif self.field == 'related_habit':
            if value and not getattr(self.instance, 'is_pleasant_habit', False):
                raise ValidationError("Связанная привычка может быть указана только для приятных привычек.")

        # Проверка частоты выполнения привычки
        elif self.field == 'frequency':
            if value < 7:
                raise ValidationError("Частота выполнения привычки не может быть меньше 7 дней.")
            elif value > 7:
                raise ValidationError("Частота выполнения привычки не может быть больше 7 дней.")

        # Проверка времени последнего выполнения привычки
        elif self.field == 'last_completed':
            if value:
                time_since_last_completed = timezone.now() - value
                if time_since_last_completed.days > 7:
                    raise ValidationError("Привычка должна быть выполнена хотя бы один раз в течение 7 дней.")

    def set_instance(self, instance):
        self.instance = instance
