from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from . serializers import UserSerializer

# Create your views here.


class CreateUserView(CreateAPIView):
    """
    To create new user on the server
    """

    # Just to configure which serializers class to implement this view
    serializer_class = UserSerializer
