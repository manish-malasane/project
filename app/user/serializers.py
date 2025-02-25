from rest_framework import serializers

# from app.core.models import User
from django.contrib.auth import get_user_model, authenticate


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User Model which we define under core application
    """

    class Meta:
        """
        Model which changes the behaviour of our custom Serializer class
        Helps to define our class
        like
        we can configure model, fields and etc...
        """

        # model = User
        model = get_user_model()

        # fields = "__all__"
        fields = ["email", "password", "name"]

        # automatically provide extra validation on ``fields`` directive when try to hit post request from browser
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "email": {"min_length": 5},
        }

    def create(self, validated_data):
        """
        Overriding Parent class Method
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Over-riding parent class update method
        """

        password = validated_data.pop("password", None)

        # Reusing parent class method
        user = super().update(instance, validated_data)

        if (
            password
        ):  # If password then update from here otherwise update everything from parent class
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for user-authentication token
    """

    email = serializers.EmailField()

    # trim_whitespace is a directive to trim whitespaces default it is True but here we set False
    # To capture whitespaces in password
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, data):
        """
        Validate and authenticate the user
        """

        # data is a dict
        email = data.get("email")

        if email.isupper():  # if email domain name is in upper format will get error
            raise serializers.ValidationError("Email is not as per standards")

        password = data.get("password")

        # authenticate method takes request which comes from `self.context.get("request")`
        # and also takes credentials
        user = authenticate(
            self.context.get("request"), username=email, password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Unable to authenticate user with given credentials",
                code="authorization",
            )  # code is HTTP code not more than that

        data["user"] = user
        return data
