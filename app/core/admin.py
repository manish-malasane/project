from django.contrib import admin  # noqa

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import JobTitle, JobDescription, Applicant, Portal

# TODO
# refer
# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/actions/#adding-actions-to-the-modeladmin

#  TODO - refer -
#  https://docs.djangoproject.com/en/4.1/topics/i18n/translation/
# https://docs.djangoproject.com/en/4.1/topics/i18n/translation/#internationalization-in-python-code
#  Required to globalize our project
#  Required for translation

from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    # This is for on what basis we want our user list
    ordering = ("id",)

    # This is for which fields we want to display on admin-page
    list_display = ("email", "name")

    # This is for which fields we want on django admin site when we try to edit the user
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Information"), {"fields": ("name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important Dates"), {"fields": ("last_login",)}),
    )

    # This is for which fields we want only in read-only format
    readonly_fields = ["last_login"]

    #  This directive is for which fields we want when creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(get_user_model(), UserAdmin)  # registering the custom user model
admin.site.register(Portal)
admin.site.register(JobDescription)
admin.site.register(JobTitle)
admin.site.register(Applicant)
