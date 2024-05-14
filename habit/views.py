from rest_framework import generics
from asgiref.sync import sync_to_async
from habit.models import Habit
from habit.paginators import HabitPaginator
from habit.serializers import HabitSerializer
from django.apps import apps


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    @staticmethod
    @sync_to_async
    def get_all_habits():
        habit = apps.get_model('habit', 'Habit')
        return list(habit.objects.all())


class HabitCreateAPIView(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    # def perform_update(self, serializer):
    #     instance = serializer.save()
    #     # Вызываем задачу Celery для отправки уведомлений об обновлении курса
    #     send_course_update_notification.delay(instance.id)


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
