from rest_framework.serializers import ModelSerializer
from .models import CustomUser, Comment, Review, News, Award, Movie, Industry, Genre, StreamingPlatform



class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content_type', 'object_id', 'content', 'timestamp']


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'content_type', 'title', 'streaming_platform', 'cast', 'director', 'content', 'plot', 'acting', 'characters', 'storytelling', 'verdict', 'publisher', 'image', 'timestamp']

class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'director', 'producer', 'release_date', 'genre', 'industry', 'streaming_platform', 'cast', 'publisher', 'timestamp']

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'content', 'publisher', 'timestamp']

class AwardSerializer(ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'title', 'image', 'content', 'publisher', 'timestamp']

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class IndustrySerializer(ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name']

class StreamingPlatformSerializer(ModelSerializer):
    class Meta:
        model = StreamingPlatform
        fields = ['id', 'name']

class CustomUserSerializer(ModelSerializer):
    liked_review = ReviewSerializer(many=True, read_only=True)
    saved_review = ReviewSerializer(many=True, read_only=True)
    liked_new = NewsSerializer(many=True, read_only=True)
    saved_new = NewsSerializer(many=True, read_only=True)
    liked_awards = AwardSerializer(many=True, read_only=True)
    saved_awards = AwardSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email_address', 'username', 'gender', 'country', 'is_active', 'is_staff', 'is_superuser', 'liked_review', 'saved_review', 'liked_new', 'saved_new', 'liked_awards', 'saved_awards']