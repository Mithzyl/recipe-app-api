from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from recipe import serializers
from core.models import Tag, Ingredient, Recipe


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


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Manage recipes in the database
    """
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        Retrieve the recipes for the authenticated user
        :return:
        """
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        Return a appropriate serializer class
        :return:
        """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new recipe
        :param serializer:
        :return:
        """
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')  # detail: specific items
    def upload_image(self, request, pk=None):
        """
        Upload an image to a recipe
        :param request:
        :param pk:
        :return:
        """
        recipe = self.get_object()  # get object based on the id in the url
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        # validation pass
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_200_OK
            )

        # validation not pass
        return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )
