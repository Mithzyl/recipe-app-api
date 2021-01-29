from .. import models
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch


def sample_user(email="Test@test.com", password="testpass"):
    """
    Create a sample user
    :param email:
    :param password:
    :return:
    """
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """
        Test the tag string representation
        :return:
        """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """
        Test the ingredient string representation
        :return:
        """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber',
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """
        Test the recipe string representation
        :return:
        """
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')  # generate a unique uuid4
    def test_recipe_file_name_uuid(self, mock_uuid):
        """
        Test that image is saved in the correct location
        :return:
        """
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')  # will remove the name of the image but \
                                                                        # remain the form of the image
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)