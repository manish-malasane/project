from django.contrib import admin  # noqa

# Register your models here.
from .models import User

admin.site.register(User)    # registering the custom user model
