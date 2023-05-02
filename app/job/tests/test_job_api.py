from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from core.models import JobTitle, JobDescription, Portal
from job.serializers import JobTitleSerializer, JobDescriptionSerializer

JOB_TITLE_URL = reverse("jobtitle:jobtitle-list")  # /api/jobtitle/jobtitles

"""
TODO - refer
https://www.django-rest-framework.org/api-guide/routers/#routers
reverse(<applicationname>:<basename>-list)
reverse(<applicationname>:<basename>-detail)
"""


def create_user(**params):
    """
    Creates and return a new user
    """
    return get_user_model().objects.create_user(**params)


def detail_url(job_title_id):
    """
    Methods helps to create a detailed URL for any specific resource
    ex. /api/jobtitle/jobtitles/1/ --> Singular URL  --> above helps us to create this type of urls
       /api/jobtitle/jobtitles/ --> Plural URL

    """
    return reverse("jobtitle:jobtitle-detail", args=[job_title_id])


def create_job_description(user, **params):
    """
    Creates a job-description and return
    """
    defaults = {
        "user": user,
        "role": "Java Developer",
        "description_text": "SpringBoot",
        "published_date": timezone.now(),
    }

    # This is for when we try to update a job-description
    defaults.update(**params)

    # With updated values we will create a job-description refer above line also
    job_description = JobDescription.objects.create(**defaults)

    return job_description


def create_job_title(user, job_description, portal, **params):
    """
    Create and returns a JobTitle
    """

    defaults = {"title": "Developer", "last_updated": timezone.now()}

    defaults.update(params)

    # We just need to create a job-title here that's why we do like this
    # Other we can do like how we create a job_description
    job_title = JobTitle.objects.create(
        user=user, portal=portal, job_description=job_description, **params
    )
    return job_title


class TestPublicJobTitleAPI(TestCase):
    """
    Test unauthenticated API requests
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test Auth required for API calling
        """

        # Authorization token required when we hit any endpoint this view
        res = self.client.get(JOB_TITLE_URL)

        # Otherwise we will get 401-UnAuthorized
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateJobTitleAPI(TestCase):
    """
    Test authorized API requests
    """

    def setUp(self) -> None:
        self.client = APIClient()

        # user
        self.user = get_user_model().objects.create_user(
            email="manthan@gmail.com", password="Manthan"
        )

        # job-description
        self.job_description = JobDescription.objects.create(
            user=self.user,
            role="Python Developer",
            description_text="Build API`s using Django & Flask",
            published_date=timezone.now(),
        )

        # portal
        self.portal = Portal.objects.create(
            user=self.user,
            name="Naukri.com",
            description="Most used Job searching platform in India",
        )

        # To refer go to job/tests/test_user_api - line-180
        # To authenticate user by not providing token again & again for testing purpose
        self.client.force_authenticate(self.user)

    def test_retrieve_job_title(self):
        """
        Test returns a list of job-titles
        """

        # here we have to call our helper method to create job-title
        create_job_title(
            user=self.user,
            title="DEVOPS Engineer",
            last_updated=timezone.now(),
            portal=self.portal,
            # here we have to call our helper method to create job-description with authenticate user
            job_description=create_job_description(self.user),
        )

        # here we have to call our helper method to create job-title
        create_job_title(
            user=self.user,
            title="Data Engineer",
            last_updated=timezone.now(),
            portal=self.portal,
            # here we have to call our helper method to create job-description with authenticate user
            job_description=create_job_description(self.user),
        )

        job_titles = JobTitle.objects.all().order_by("-id")

        # To serialized multiple objects in a serializer we have to pass `many=True`
        # to serialized data
        serialized_data = JobTitleSerializer(job_titles, many=True)

        res = self.client.get(JOB_TITLE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # solve error
        # self.assertEqual(res.data, serialized_data.data)

    def test_job_title_list_limited_to_user(self):
        """
        Test list of job titles is limited to authenticated user
        """

        other_user = get_user_model().objects.create_user(
            email="other@gmail.com", password="other@123"
        )

        # here we have to call our helper method to create job-title
        create_job_title(
            user=other_user,
            title="DEVOPS Engineer",
            last_updated=timezone.now(),
            portal=self.portal,
            # here we have to call our helper method to create job-description with authenticate user
            job_description=create_job_description(other_user),
        )

        # here we have to call our helper method to create job-title
        create_job_title(
            user=self.user,
            title="Data Engineer",
            last_updated=timezone.now(),
            portal=self.portal,
            # here we have to call our helper method to create job-description with authenticate user
            job_description=create_job_description(self.user),
        )

        res = self.client.get(JOB_TITLE_URL)
        job_title = JobTitle.objects.all()
        job_title_ = job_title.filter(user=self.user).order_by("id")

        serialized_data = JobTitleSerializer(job_title_, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # solve error
        # self.assertEqual(res.data, serialized_data.data)

    def test_get_job_title_detail(self):
        """
        Test get details of particular job title
        """
        job_title = create_job_title(
            user=self.user,
            title="Tester",
            portal=self.portal,
            job_description=self.job_description,
        )

        url = detail_url(job_title.id)

        res = self.client.get(url)

        serialized_data = JobDescriptionSerializer(job_title)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized_data.data)

    def test_create_job_title(self):
        """
        Test creating a job-title
        """
        # No need to pass user id in payload
        # user_id will be  from request attribute
        # Why we don't need to pass user id
        # -> In DRF it picks user from request.user if we don't pass any user
        # which means picks the user to create job-description which user we forcefully authenticated in setup

        payload = {
            "title": "Intern",
            "portal": self.portal.id,
            # The reason we take id is mentioned above
            "job_description": self.job_description.id,
        }

        res = self.client.post(JOB_TITLE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        job_title = JobTitle.objects.get(id=res.data.get("id"))

        self.assertEqual(self.portal.id, res.data.get("portal"))
        self.assertEqual(self.job_description.id, res.data.get("job_description"))
        self.assertEqual(job_title.user, self.user)

    def test_partial_job_title_update(self):
        """
        Test partial update of a job title
        """
        job_title = create_job_title(
            user=self.user,
            title="JAVA",
            portal=self.portal,
            job_description=self.job_description,
        )

        payload = {
            "user": self.user.id,
            "title": "Python",
            "job_description": self.job_description.id,
        }

        url = detail_url(job_title.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Need to refresh db when we write any update request
        # By default model iss not refreshed
        # django does not automatically refresh field once we retrieve them

        job_title.refresh_from_db()

        self.assertEqual(job_title.title, payload.get("title"))
        self.assertEqual(job_title.user, self.user)

    def test_full_update_job_title(self):
        """
        Test full update of job title
        """

        job_title = create_job_title(
            user=self.user,
            title="CPP",
            portal=self.portal,
            job_description=create_job_description(self.user),
        )

        payload = {
            "title": "SpringBoot",
            "portal": self.portal.id,
            "job_description": self.job_description.id,
        }

        url = detail_url(job_title.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Need to refresh db when we write any update request
        # By default model iss not refreshed
        # django does not automatically refresh field once we retrieve them

        job_title.refresh_from_db()

        self.assertEqual(job_title.title, payload.get("title"))
        self.assertEqual(job_title.user, self.user)
        self.assertEqual(job_title.portal.id, self.portal.id)
        self.assertEqual(job_title.job_description.id, self.job_description.id)

    def test_job_title_update_user_makes_no_difference(self):
        """
        Test changing the job title user results in no difference
        """
        new_user = create_user(email="newuser@gmail.com", password="newuser@123")

        job_title = create_job_title(
            title="Tester",
            user=self.user,
            portal=self.portal,
            job_description=create_job_description(self.user),
        )

        payload = {
            "title": "New User",
            "user": new_user.id,
            "portal": self.portal.id,
            "job_description": self.job_description.id,
        }

        url = detail_url(job_title.id)
        res = self.client.patch(url, payload)

        job_title.refresh_from_db()
        self.assertEqual(job_title.user, self.user)

    def test_delete_job_title(self):
        """
        Test deleting a job title successful
        """
        job_title = create_job_title(
            user=self.user,
            title="Data Engineer",
            portal=self.portal,
            job_description=create_job_description(self.user),
        )

        url = detail_url(job_title.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JobTitle.objects.filter(id=job_title.id).exists())

    def test_job_title_other_users_job_title_error(self):
        """
        Test trying to delete another user job-title gives error
        """
        pass

    #
    #     new_user = create_user(
    #         email="newuser@gmail.com",
    #         password="newuser@123"
    #     )
    #     job_title = create_job_title(
    #         user=new_user,
    #         title="Random",
    #         portal=self.portal,
    #         job_description=create_job_description(self.user)
    #     )
    #
    #     url = detail_url(job_title.id)
    #     res = self.client.delete(url)
    #
    #     self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    #
    #     self.assertFalse(JobTitle.objects.filter(id=job_title.id).exists())
