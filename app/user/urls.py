"""
URL mapping for user-API

1) /api/user/           --> To get list of users
2) /api/user/create/    --> To create new user
3) /api/user/me/        --> To get description of the user
"""

from django.urls import path
from . views import CreateUserView

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),

]
