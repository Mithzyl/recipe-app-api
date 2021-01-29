from rest_framework import serializers
from core.models import Ingredient, Tag, Recipe


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for tag objects
    """
    class Meta:
        model = Tag
        fields = ('id', 'name')
        # read_only_fields = ('id',)
        extra_kwargs = {'id': {'read_only': True}}


class IngredientSerializer(serializers.ModelSerializer, ):
    """
    Serializer for ingredient objects
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        extra_kwargs = {'id': {'read_only': True}}


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serialize a recipe
    """
    # Foreign key fields
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags',
                  'time_minutes', 'price', 'link')
        extra_kwargs = {'id': {'read_only': True}}


class RecipeDetailSerializer(RecipeSerializer):
    """
    Serialize a recipe detail
    """
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
