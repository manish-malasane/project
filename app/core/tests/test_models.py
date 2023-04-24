from django.test import TestCase

# from ..models import User
from django.contrib.auth import get_user_model


class TestModel(TestCase):
    def random(self):
        return "Python"

    def test_func(self):
        expected = "Java", "JavaScript", "Python"
        res = self.random()

        # https://docs.python.org/3/library/unittest.html#assert-methods
        # to check value membership using In
        self.assertIn(res, expected)

        # to check value membership using NotIn
        # self.assertNotIn(res, expected)

    def test_create_user_with_email_successful(self):
        """
        Test for creating user account
        """
        email = "mmalasane6@gmail.com"
        password = "qwerty"

        # user = User.objects.create_user(email=email,
        #                                 password=password)

        user = get_user_model().objects.create_user(email=email, password=password)

        # `user.email` is an expected email and `email` is an actual email.
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test for normalization of email if user
        made mistake while entering the email
        """
        password = "admin"
        emails = [
            ["aDmin1@Gmail.com", "aDmin1@gmail.com"],
            ["ADmin2@gmail.com", "ADmin2@gmail.com"],
            ["ADMIN3@GMAIl.COM", "ADMIN3@gmail.com"],
        ]

        for email, expected_email in emails:
            user = get_user_model().objects.create_user(email, password)

            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """
        Test for creation of user who is trying
        to create account without email-address
        """
        # 1ST SCENARIO
        self.assertRaises(
            ValueError, get_user_model().objects.create_user, "", "password"
        )

        # WE CAN DO EITHER 1ST SCENARIO OR 2ND SCENARIO

        # 2ND SCENARIO
        # with self.assertRaises(ValueError):
        #     get_user_model().objects.create_user("", "password")

    def test_create_superuser(self):
        """
        Test for creation of superuser
        """
        email = "email@gmail.com"
        password = "password"
        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
