from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe import serializers
from core.models import Tag, Ingredient


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    Base viewset for user owned recipe attributes
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        Return objects for the current authenticated user only
        :return:
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """
        Create a new object
        :param serializer:
        :return:
        """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """
    Manage tags in the database
    """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()



class IngredientViewSet(BaseRecipeAttrViewSet):
    """
    Manage ingredients in the database
    """
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

