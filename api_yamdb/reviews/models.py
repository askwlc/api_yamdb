from django.contrib.auth.models import AbstractUser
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
