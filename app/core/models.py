from django.db import models  # noqa

# Create your models here
# TODO - Prefer for understanding
# Customization of default authentication system in django
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#a-full-example

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.conf import settings
from django.utils import timezone


class UserManager(BaseUserManager):  # customizing default UserManager class
    def create_user(
        self, email: str, password=None, **extra_fields
    ):  # to create and save user
        """
        create, saves and returns a new user
         Args:
            email (str): will be set as new default value for `username` field
            password: encrypted password via hashing
            **extra_fields: arbitrary keyword arguments to acmodate
            any additional user attributes
        Returns:
            user object
        """
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


class Portal(models.Model):
    """
    Portal table for various job portals
     # TODO - refer
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#field-types
    alternate ways for defining foreign key relation with user model are
    1) from django.contrib.auth import get_user_model
    2) from core.models import User (This already present here actually)
    3) from django.conf import settings (Which we use)
    """

    # `on_delete=models.CASCADE` is for if any user deletes his/her account
    # so all info he/she added will delete from our application
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)

    def __str__(self):
        """
        If id need
        str(self.id) + "portal" + self.name INSTEAD of self.name
        Refer -
        https://github.com/prashant5nov/project1/blob/main/app/core/models.py
        """
        return self.name


class JobDescription(models.Model):
    """
    Table for JobDescription of JobTitle
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    role = models.CharField(max_length=50)
    description_text = models.CharField(max_length=250)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.role} - ({self.published_date})"


class JobTitle(models.Model):
    """
    JobTitle :- will have associated with multiple portals
    JobTitle <--> Portal (OneToManyField Relationship)
        One JobTitle can on multiple portals
    JobTitle <--> JobDescription  (OneToOneField Relationship)
        One JobTitle will have only one JobDescription
     # TODO
    # refer
    # https://docs.djangoproject.com/en/4.1/topics/db/examples/#examples-of-model-relationship-api-usag
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=25)
    last_updated = models.DateTimeField(default=timezone.now)

    # OneToOneField Relationship
    job_description = models.OneToOneField(JobDescription, on_delete=models.CASCADE)

    # OneToManyField Relationship
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - ({self.portal})"


class Applicant(User):
    """
    - Whoever is user by default his/her applicant status will True
    - here we don't need to define ApplicantNameField because it's already in parent class
    - again here we also don't need to specify foreignkey relationship with user
    because here already we inherit this model from user model
    """

    is_applicant = models.BooleanField(default=True)

    # OneToManyField Relationship
    applied_for = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    cover_letter = models.CharField(max_length=150)

    def __str__(self):
        return self.name
