from django.core.exceptions import ValidationError
from django.utils import timezone


class OnlyOneFieldValidator:
    def __call__(self, instance):
        if instance.is_pleasant_habit:
            if instance.related_habit:
                raise ValidationError("Поле 'связанная привычка' не может быть заполнено.")
            if instance.reward:
                raise ValidationError("Поле 'вознаграждение' не может быть заполнено.")


class RelatedHabitValidator:
    def __call__(self, instance):
        if not instance.is_pleasant_habit:
            raise ValidationError("Связанная привычка может быть указана только для приятных привычек.")


class PleasantHabitValidator:
    def __call__(self, instance):
        if instance.related_habit and instance.related_habit.is_pleasant:
            if instance.reward or instance.related_habit:
                raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")


class FrequencyValidator:
    def __call__(self, instance):
        if instance.frequency < 1 or instance.frequency > 7:
            raise ValidationError("Частота выполнения привычки должна быть от 1 до 7 дней.")
