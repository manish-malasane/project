from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


class TestAdminSite(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="australia@gmail.com", password="pass@123"
        )

        # alternate way of login but we use force login
        # cause here we have to pass credentials
        # and in force_login we just wanted to tell which user we want to login

        # self.client.login(email="steve@gmail.com",
        #                   password="pass@123")

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="steve@gmail.com", password="pass@123"
        )

    def test_user_list(self):
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_edit_user_page(self):
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_create_user(self):
        url = reverse("admin:core_user_add")

        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_to_see_user_page_history(self):
        url = reverse("admin:core_user_history", args=[self.user.id])

        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_to_delete_user(self):
        url = reverse("admin:core_user_delete", args=[self.user.id])

        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)
