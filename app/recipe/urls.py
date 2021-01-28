import sys
from django.urls import path, include
from rest_framework.routers import DefaultRouter

sys.path.append(".")
from . import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]