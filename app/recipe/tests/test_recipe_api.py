from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipe:recipe-list')


# /api/recipe/recipes
# /api/recipe/recipes/1(id)
def detail_url(recipe_id):
    """
    Return recipe detail URL
    :param recipe_id:
    :return:
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Main course'):
    """
    Create and return a sample tag
    :param user:
    :param name:
    :return:
    """
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    """
    Create and return a sample ingredient
    :param user:
    :param name:
    :return:
    """
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """
    Create a sample recipe
    :param user:
    :param params:
    :return:
    """
    defults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00,
    }
    defults.update(params)

    return Recipe.objects.create(user=user, **defults)


class PublicRecipeApiTests(TestCase):
    """
    Test unauthorized recipe API access
    """
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is required
        :return:
        """
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """
    Test unauthenticated recipe API access
    """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testprivaterecipe@test.com",
            password="testpass"
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """
        Test retrieving a list of recipes
        :return:
        """
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """
        Test retrieving recipes for user
        :return:
        """
        user2 = get_user_model().objects.create_user(
            email="othertestprivaterecipe@test.com",
            password="testpass"
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """
        Test viewing a recipe detail
        :return:
        """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)