from django.db import models  # noqa

# Create your models here
# TODO - Prefer for understanding
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#a-full-example

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):  # customizing default UserManager class
    def create_user(
        self, email: str, password=None, **extra_fields
    ):  # to create and save user
        if not email:
            raise ValueError("Email is Must for user")

        # using built-in functionality to normalize the email
        # with `self.model` we are already associated with default user model
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # using built-in functionality to set user password
        user.set_password(password)
        user.save(
            using=self._db
        )  # to save user when we are interacting with multiple databases
        return user

    def create_superuser(self, email, password):  # to create superuser
        """https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=251)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # whatever ORM queries we run
    # all goes through these objects attribute User.objects.get()
    objects = UserManager()

    # to define new USERNAME_FIELD in custom user model
    USERNAME_FIELD = "email"
