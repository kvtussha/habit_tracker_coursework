from rest_framework import generics
from asgiref.sync import sync_to_async

from habit.management.commands import habits_reminder
from habit.models import Habit
from habit.paginators import HabitPaginator
from habit.serializers import HabitSerializer
from users.models import User


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    @sync_to_async
    def get_all_habits(self):
        queryset = Habit.objects.all()
        return list(queryset)

    @sync_to_async
    def get_all_user_habits(self, user_tg_id):
        user = User.objects.get(bot_id=user_tg_id)
        queryset = Habit.objects.filter(user=user)
        return list(queryset)


class HabitCreateAPIView(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    @staticmethod
    @sync_to_async
    def perform_retrieve(habit_id):
        habit = Habit.objects.get(id=habit_id)
        return habit


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_update(self, serializer):
        # Вызываем задачу Celery для отправки уведомлений об обновлении курса
        habits_reminder.apply_async(countdown=5)


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    @sync_to_async
    def perform_destroy(self, habit_id):
        habit = Habit.objects.get(id=habit_id)
        habit.delete()
