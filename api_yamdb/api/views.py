from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings

from .filters import TitleFilter
from .paginator import CommentPagination
from .permissions import AuthorAndStaffOrReadOnly, IsAdmin, IsAdminOrReadOnly, IsAuthorOrModeRatOrOrAdminOrReadOnly
from .serializers import (CommentsSerializer, ReviewsSerializer,
                          GenreSerializer, CategorySerializer,
                          TitleSerializer,
                          RegistrationSerializer, GetTokenSerializer, UserSerializer, UserEditSerializer,
                          TitlePostSerializer)
from reviews.models import Genre, Category, Title, User
from api.mixins import CustomSet


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    pagination_class = CommentPagination
    search_fields = ('username',)

    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserEditSerializer(user)
        if request.method == 'PATCH':
            serializer = UserEditSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CommentPagination
    filterset_class = TitleFilter
    filterset_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitlePostSerializer
        return TitleSerializer


class GenreViewSet(CustomSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CustomSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = CommentPagination
    permission_classes = [IsAuthorOrModeRatOrOrAdminOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = CommentPagination
    permission_classes = [IsAuthorOrModeRatOrOrAdminOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('У произведения нет такого отзыва')
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('У произведения нет такого отзыва')
        serializer.save(author=self.request.user, review=review)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if User.objects.filter(
                username=request.data.get('username'),
                email=request.data.get('email')
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        try:
            user, create = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            raise ValidationError('Неправильное имя пользователя или email')
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация на Yamdb',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.ADMIN_EMAIL,
            recipient_list=[user.email],
        )
        return Response(confirmation_code, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(
            User,
            username=username,
        )
        if user.confirmation_code != confirmation_code:
            return Response(
                'Неправильный код подтверждения',
                status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response(
            {'access_token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )
