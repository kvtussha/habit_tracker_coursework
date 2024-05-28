from django.urls import path

from users.views import UserListAPIView, UserRetrieveAPIView, UserCreateAPIView

app_name = 'users'

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('user/detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('user/create', UserCreateAPIView.as_view(), name='user-create'),
]
