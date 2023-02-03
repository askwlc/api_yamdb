from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router = DefaultRouter()
router.register('tittle', TitleViewSet)
router.register('genre', GenreViewSet)
router.register('category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]