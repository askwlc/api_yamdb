from rest_framework import serializers

from api_yamdb.reviews.models import Title, Category, Genre


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)