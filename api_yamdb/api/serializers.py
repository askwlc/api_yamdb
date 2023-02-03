from rest_framework import serializers

from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review, Title, Category, Genre


class ReviewsSerializer(serializers.ModelSerializer):
    """Ревью для произведений"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ['title']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            user = self.context['request'].user
            if user.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )
        return data

    def validate_score(self, value):
        if 0 >= value >= 10:
            raise serializers.ValidationError('Проверьте оценку')
        return value
    

class CommentsSerializer(serializers.ModelSerializer):
    """Комментарии на отзывы"""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


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


class RegistrationSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class GetTokenSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
