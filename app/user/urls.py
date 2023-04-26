"""
URL mapping for user-API

1) /api/user/           --> To get list of users
2) /api/user/create/    --> To create new user
3) /api/user/me/        --> To get description of the user
"""

from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
]
