from rest_framework import generics
from asgiref.sync import sync_to_async

from habit.tasks import habits_reminder
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
        instance = serializer.save()
        obj = {
            "user": instance.user.id,
            "title": instance.title,
            "place": instance.place,
            "time": instance.time.strftime('%H:%M'),
            "action": instance.action,
            "is_pleasant_habit": instance.is_pleasant_habit,
            "is_useful_habit": instance.is_useful_habit,
            "related_habit": instance.related_habit.id if instance.related_habit else None,
            "frequency": instance.frequency,
            "reward": instance.reward,
            "time_to_complete": instance.time_to_complete,
            "is_public": instance.is_public,
        }
        habits_reminder.delay(obj)


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    @sync_to_async
    def perform_destroy(self, habit_id):
        habit = Habit.objects.get(id=habit_id)
        habit.delete()
