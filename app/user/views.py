from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.


class CreateUserView(CreateAPIView):
    """
    To create new user on the server
    """

    # Just to configure which serializers class to implement this view
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    View to generate token if given payload
    credentials are correct

    TODO-Refer
    https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
    """

    # Over-riding serializer_class variable with our custom serializer
    serializer_class = AuthTokenSerializer
