
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, ReviewViewSet, TitleViewSet, GenreViewSet, CategoryViewSet

app_name = 'api'

router = DefaultRouter()

router.register('tittle', TitleViewSet)
router.register('genre', GenreViewSet)
router.register('category', CategoryViewSet)

router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router.urls)),
]

