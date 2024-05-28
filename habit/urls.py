from django.urls import path

from habit.views import HabitListAPIView, HabitRetrieveAPIView, HabitCreateAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView

app_name = 'habits'

urlpatterns = [
    path('', HabitListAPIView.as_view(), name='habit-list'),
    path('habit/detail/<int:pk>', HabitRetrieveAPIView.as_view(), name='habit-detail'),
    path('habit/create', HabitCreateAPIView.as_view(), name='habit-create'),
    path('user/update/<int:pk>', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('user/delete/<int:pk>', HabitDestroyAPIView.as_view(), name='habit-create'),
]
