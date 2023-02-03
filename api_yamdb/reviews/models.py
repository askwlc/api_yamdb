from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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


class Title(models.Model):
    """Модель произведений, к которым пишут отзывы."""
    category = models.ForeignKey(
        'Category', verbose_name='Категория',
        on_delete=models.SET_NULL, null=True
    )
    genre = models.ManyToManyField('Genre', verbose_name='Жанр')
    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveSmallIntegerField('Год выпуска', )
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категорий (типов) произведений."""
    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField('Имя жанра', max_length=256)
    slug = models.SlugField('Slug', max_length=50, unique=True)

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

