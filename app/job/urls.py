from django.urls import path
from app1.job import views

url_patterns = [
    path("job-title/", views.JobTitleViewSet.as_view({"get": "list"}), name="Titles")
]
