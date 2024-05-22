import random
import string

from rest_framework import generics
from users.models import User
from users.serializers import UsersSerializer
from asgiref.sync import sync_to_async


class UserListAPIView(generics.ListAPIView):
    serializer_class = UsersSerializer
    queryset = User.objects.all()

    @sync_to_async
    def get_all_bot_ids(self):
        users = list(self.get_queryset())
        ids = []
        for user in users:
            ids.append(user.bot_id)
        return ids


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UsersSerializer
    queryset = User.objects.all()

    @staticmethod
    @sync_to_async
    def create_user(username, phone, bot_id):
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for _ in range(8))
        User.objects.create(username=username, phone=phone, bot_id=bot_id, password=password)

