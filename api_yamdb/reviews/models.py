from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime as dt
from django.db import models
from django.conf import settings


class User(AbstractUser):
    """Переопределение полей стандартной модели User"""
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        choices=settings.ROLE_CHOICES,
        max_length=10, default='USER'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )

    confirmation_code = models.CharField(
        max_length=settings.CONFIRMATION_CODE_MAX_LENGTH,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        """True для пользователей с правами модератора."""
        return self.role == settings.MODERATOR_ROLE

    @property
    def is_admin(self):
        """True для пользователей с правами админа и суперпользователей."""
        return (
            self.role == settings.ADMIN_ROLE
            or self.is_staff
            or self.is_superuser
        )


class Title(models.Model):
    """Модель произведений, к которым пишут отзывы."""
    category = models.ForeignKey(
        'Category', verbose_name='Категория',
        on_delete=models.SET_NULL, null=True
    )
    genre = models.ManyToManyField('Genre', verbose_name='Жанр')
    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[MinValueValidator(
            limit_value=1,
            message="Год не может быть меньше или равен нулю"),
            MaxValueValidator(
                limit_value=dt.date.today().year,
                message="Год не может быть больше текущего года")])
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = "titles"


    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категорий (типов) произведений."""
    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = "categories"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField('Имя жанра', max_length=256)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = "genres"

    def __str__(self):
        return self.name

class Review(models.Model):
    """Модель отзывы и рейтинг"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review")
        ]


class Comment(models.Model):
    """Модель комментариев"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()

    def __str__(self):
        return self.author

