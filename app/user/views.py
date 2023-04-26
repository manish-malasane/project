from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
)  # DRF Generics for CRUD operations
from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
)  # Custom serializers (ModelSerializers)
from rest_framework.authtoken.views import ObtainAuthToken  # For TokenAuthentication
from rest_framework import (
    authentication,
    permissions,
)  # This is authentication for any specific view

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


class ManageUserView(RetrieveUpdateAPIView):
    """
    This view helps us to perform following http methods
    - GET
    - PUT
    - PATCH

    TODO
    refer -
    https://www.django-rest-framework.org/api-guide/generic-views/#retrieveupdateapiview
    """

    # Configuring which serializer we need for that over-riding this directive
    serializer_class = UserSerializer

    # In our project we use TokenAuthentication
    # Here we are over-riding `authentication_classes` directive for which type of authentication we need
    # TODO - Refer
    # https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
    authentication_classes = [authentication.TokenAuthentication]

    # Over-riding `permission_classes` directive for permission to authenticate the given
    # TODO - refer
    # https://www.django-rest-framework.org/api-guide/permissions/#setting-the-permission-policy
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve user and return authenticated user information
        TODO - refer
        https://www.django-rest-framework.org/api-guide/permissions/#object-level-permissions
        """
        return self.request.user  # helps to retrieve user who sends the request
