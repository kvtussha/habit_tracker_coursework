from rest_framework import viewsets, generics

from habit.models import Habit
from habit.paginators import HabitPaginator
from habit.serializers import HabitSerializer


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_habits(self):
        return list(self.queryset)


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