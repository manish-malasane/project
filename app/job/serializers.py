from rest_framework import serializers
from core.models import JobTitle


class JobTitleSerializer(serializers.ModelSerializer):
    """
    Serializer class for JobTitle ListView
    """

    class Meta:
        """
        This class is for changing the behaviour of our serializer
        and this class helps use to define ModelSerializer
        like fields, model,  etc...
        """

        model = JobTitle
        fields = ["id", "title"]
        read_only_fields = ["id"]


class JobDescriptionSerializer(JobTitleSerializer):
    """
    Serializer class for JobTitle detail view
    this is for if our ``self.action != "list"``

    Here we are reusing the functionality which written under JobTitleSerializer
    -- Writing Nested ModelSerializers
    TODO - Refer
    https://www.django-rest-framework.org/api-guide/serializers/#overriding-serialization-and-deserialization-behavior
    """

    class Meta(JobTitleSerializer.Meta):
        """
        This ModelSerializer we are inheriting from JobTitleSerializer, so we need
        Parent Class Meta here and to capture parent class meta
        we do
        ``class Meta(<ParentSerializer>.Meta)``
        """

        # To capture ParentModelSerializer fields in ChildModelSerializer
        # we have use below logic
        #  fields = ParentModelSerializer.Meta.fields + [
        #             "field1-from-child-serializer", "field2-from-child-serializer", etc..]
        fields = JobTitleSerializer.Meta.fields + ["job_description", "portal"]
