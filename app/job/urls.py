from django.urls import path, include
from job import views

# "DefaultRouter" for automatic URL mapping with views in regex pattern
# TODO - Refer
# https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
from rest_framework.routers import DefaultRouter


# Initialization of DefaultRouter
router = DefaultRouter()

# This app_name will be utilized when we use reverse function for named urls
app_name = "jobtitle"


# `jobtitles` is a basename
# `jobtitles` is also a url `/api/job/jobtitles/`
# router.register("jobtitles/", views.JobTitleViewSet) <-- we also can add trailing slash here

router.register("jobtitles", views.JobTitleViewSet)

# we also can add url suffix here ``urlpatterns = [path("job/", include(router.urls))]``
urlpatterns = [path("", include(router.urls))]


# Without Regex (Manually)
# urlpatterns = [
#     # {"post": "create"} and etc... for all types of HTTP methods
#     path("jobtitle/", views.JobTitleViewSet.as_view({"get": "list"}), name="Titles")
# ]
