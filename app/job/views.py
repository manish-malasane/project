from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import JobTitleSerializer, JobDescriptionSerializer
from app.core.models import JobTitle


class JobTitleViewSet(viewsets.ModelViewSet):
    """
    This is the ViewSet of JobTitle for all types of
    actions(list, retrieve, update, destroy, etc..)
    """

    # Over-riding `serializer_class` with our own serializer class
    serializer_class = JobDescriptionSerializer

    # Over-riding `queryset` with our own data which we get when we perform ORM query
    queryset = JobTitle.objects.all()

    # So now we Over-ride `serializer_class` & `queryset`
    # so we need to write methods corresponding to this

    def get_serializer_class(self):
        """
        If user hits list(Plural) endpoint which is list so user get the list of JobTitles
                if self.action == "list":
                    return JobTitleSerializer
            (Singular)otherwise user get JobDescription of particular JobTitle
                    return self.serializer_class (serializer_class which we configure as JobDescriptionSerializer)

        Plural - localhost/api/job/job-title/
        Singular - localhost/api/job/job-title/15
        """

        if self.action == "list":
            return JobTitleSerializer

        return self.serializer_class

    def get_queryset(self):
        """
        Filtering the results only for user.
        User will only see whichever data he/she posted

        And that will order by descending order because we do
                order_by("-id")
        And if we need data in ascending order we do
                order_by("id")
        """
        return self.queryset.filter(user=self.request.user).order_by("-id")
