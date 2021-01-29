from rest_framework import serializers
from core.models import Ingredient, Tag


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


