from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from . import serializers
from ..core.models import Tag


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    Manage tags in the database
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        """
        Return objects for the current authenticated user only
        :return:
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')