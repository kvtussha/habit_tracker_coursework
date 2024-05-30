from django.urls import reverse, reverse_lazy
from rest_framework.test import APITestCase, APIClient

from habit.serializers import HabitSerializer
from users.models import User
from habit.models import Habit
from rest_framework import status


class HabitTestCase(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(email='testuser@gmail.com', username='testuser', password='password123',
                                             bot_id=5121595188)
        self.habit1 = Habit.objects.create(user=self.user, title="Habit 1", place="Place 1", time="12:00",
                                           action="Action 1",
                                           is_pleasant_habit=Habit.YES, is_useful_habit=False, related_habit=None,
                                           frequency=1, reward=None, time_to_complete=60, is_public=Habit.YES)
        self.habit2 = Habit.objects.create(user=self.user, title="Habit 1", place="Place 1", time="12:00",
                                           action="Action 1",
                                           is_pleasant_habit=Habit.YES, is_useful_habit=False, related_habit=None,
                                           frequency=1, reward=None, time_to_complete=60, is_public=Habit.YES)

        # Создаем клиент API и аутентифицируемся как тестовый пользователь
        self.client = APIClient()
        self.client2 = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        url = reverse_lazy('habits:habit-create')
        habit_data = {
            'user': self.user.pk,
            'title': "Habit 1",
            'place': "Place 1",
            'time': "12:00",
            'action': "Action 1",
            'is_pleasant_habit': Habit.YES,
            'is_useful_habit': False,
            'related_habit': None,
            'frequency': 1,
            'reward': None,
            'time_to_complete': 60,
            'is_public': Habit.YES,
        }
        response = self.client.post(url, habit_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_habits(self):
        url = reverse_lazy('habits:habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
