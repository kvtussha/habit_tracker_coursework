from django.core.exceptions import ValidationError
from django.utils import timezone


class OnlyOneFieldValidator:
    def __call__(self, instance):
        if instance.reward and instance.related_habit:
            raise ValidationError("Только одно из полей 'вознаграждение' и 'связанная привычка' может быть заполнено.")


class PleasantHabitValidator:
    def __call__(self, instance):
        if instance.related_habit and not instance.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка может быть указана только для приятных привычек.")


class NoRewardForPleasantHabitValidator:
    def __call__(self, instance):
        if instance.related_habit and instance.related_habit.is_pleasant:
            if instance.reward or instance.related_habit:
                raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")


class FrequencyValidator:
    def __call__(self, instance):
        if instance.frequency_days < 1 or instance.frequency_days > 7:
            raise ValidationError("Частота выполнения привычки должна быть от 1 до 7 дней.")


class LastPerformedValidator:
    def __call__(self, instance):
        if instance.last_performed:
            time_since_last_completed = timezone.now() - instance.last_performed
            if time_since_last_completed.days > 7:
                raise ValidationError("Привычка должна быть выполнена хотя бы один раз в течение 7 дней.")
