from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User
from habit.models import Habit
from habit.serializers import HabitSerializer


class HabitListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.habit1 = Habit.objects.create(user=self.user, title="Habit 1", place="Place 1", time="12:00",
                                           action="Action 1",
                                           is_pleasant_habit=Habit.YES, is_useful_habit=True, related_habit=None,
                                           frequency=1, reward="Reward 1", time_to_complete=60, is_public=Habit.YES)
        self.habit2 = Habit.objects.create(user=self.user, title="Habit 2", place="Place 2", time="14:00",
                                           action="Action 2",
                                           is_pleasant_habit=Habit.NO, is_useful_habit=False, related_habit=None,
                                           frequency=2, reward="Reward 2", time_to_complete=30, is_public=Habit.NO)

    def test_get_all_habits(self):
        url = reverse('habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        habits = Habit.objects.all()
        serializer = HabitSerializer(habits, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_user_habits(self):
        url = reverse('habit-list')
        response = self.client.get(url, {'user_tg_id': self.user.bot_id})
        self.assertEqual(response.status_code, 200)
        user_habits = Habit.objects.filter(user=self.user)
        serializer = HabitSerializer(user_habits, many=True)
        self.assertEqual(response.data, serializer.data)


class HabitCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")

    def test_create_habit(self):
        url = reverse('habit-create')
        data = {
            'user': self.user.id,
            'title': 'New Habit',
            'place': 'New Place',
            'time': '10:00',
            'action': 'New Action',
            'is_pleasant_habit': Habit.YES,
            'is_useful_habit': True,
            'related_habit': None,
            'frequency': 1,
            'reward': 'New Reward',
            'time_to_complete': 60,
            'is_public': Habit.YES,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().title, 'New Habit')


class HabitRetrieveAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.habit = Habit.objects.create(user=self.user, title="Test Habit", place="Test Place", time="12:00",
                                          action="Test Action",
                                          is_pleasant_habit=Habit.YES, is_useful_habit=True, related_habit=None,
                                          frequency=1, reward="Test Reward", time_to_complete=60, is_public=Habit.YES)

    def test_retrieve_habit(self):
        url = reverse('habit-detail', kwargs={'pk': self.habit.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        serializer = HabitSerializer(self.habit)
        self.assertEqual(response.data, serializer.data)


class HabitUpdateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.habit = Habit.objects.create(user=self.user, title="Test Habit", place="Test Place", time="12:00",
                                          action="Test Action",
                                          is_pleasant_habit=Habit.YES, is_useful_habit=True, related_habit=None,
                                          frequency=1, reward="Test Reward", time_to_complete=60, is_public=Habit.YES)

    def test_update_habit(self):
        url = reverse('habit-update', kwargs={'pk': self.habit.id})
        data = {
            'title': 'Updated Habit',
            'place': 'Updated Place',
            'time': '14:00',
            'action': 'Updated Action',
            'is_pleasant_habit': Habit.NO,
            'is_useful_habit': False,
            'related_habit': None,
            'frequency': 2,
            'reward': 'Updated Reward',
            'time_to_complete': 30,
            'is_public': Habit.NO,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Habit.objects.get().title, 'Updated Habit')


class HabitDestroyAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.habit = Habit.objects.create(user=self.user, title="Test Habit", place="Test Place", time="12:00",
                                          action="Test Action",
                                          is_pleasant_habit=Habit.YES, is_useful_habit=True, related_habit=None,
                                          frequency=1, reward="Test Reward", time_to_complete=60, is_public=Habit.YES)

    def test_destroy_habit(self):
        url = reverse('habit-delete', kwargs={'pk': self.habit.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 0)
