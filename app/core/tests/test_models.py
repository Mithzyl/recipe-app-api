from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_success(self):
        """
        Test creating a new user with an email successful
        :return:
        """
        email = "test@londonappdev.com"
        password = 'Testpass123'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password), password)

    def test_new_user_email_normalized(self):
        """
        Test that email for a new user is normalized
        :return:
        """
        email = 'test@LONDANAPPDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating user with no email raises error
        :return:
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Test123')

    def test_create_new_superuser(self):
        """
        Test creaing a new superuser
        :return:
        """
        user = get_user_model().objects.create_superuser('test@londonappdev.com', 'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)