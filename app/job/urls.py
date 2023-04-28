from django.urls import path
from job import views

urlpatterns = [
    path("jobtitle/", views.JobTitleViewSet.as_view({"get": "list"}), name="Titles")
]
