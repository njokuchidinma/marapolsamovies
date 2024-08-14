from rest_framework.serializers import ModelSerializer, SerializerMethodField, EmailField, CharField, Serializer
from .models import CustomUser, Comment, Review, News, Award, Movie, Industry, Genre, StreamingPlatform, NewsletterSubscription
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _


class NewsletterSubscriptionSerializer(ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['email_address', 'first_name']
        extra_kwargs = {
            'email_address': {'help_text': 'The email address of the subscriber'},
            'first_name': {'help_text': 'The first name of the subscriber'}
        }

class CommentSerializer(ModelSerializer):
    like_count = SerializerMethodField(help_text='The number of likes the comment has received')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content_type', 'object_id', 'content', 'like_count', 'timestamp']
        extra_kwargs = {
            'user': {'help_text': 'The user who made the comment'},
            'content_type': {'help_text': 'The type of content being commented on'},
            'object_id': {'help_text': 'The ID of the object being commented on'},
            'content': {'help_text': 'The content of the comment'},
            'timestamp': {'help_text': 'The time the comment was created'}
        }
    
    def get_like_count(self, obj):
        return obj.like_set.count()

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'content', 'title', 'streaming_platform', 'cast', 
            'director', 'plot', 'acting', 'characters', 
            'storytelling', 'verdict', 'publisher', 'thumbnail', 'timestamp'
        ]
        extra_kwargs = {
            'title': {'help_text': 'The title of the review'},
            'streaming_platform': {'help_text': 'The streaming platform for the reviewed content'},
            'cast': {'help_text': 'The cast involved in the content'},
            'director': {'help_text': 'The director of the content'},
            'content': {'help_text': 'The main content of the review'},
            'plot': {'help_text': 'The plot evaluation of the content'},
            'acting': {'help_text': 'The acting evaluation of the content'},
            'characters': {'help_text': 'The character evaluation of the content'},
            'storytelling': {'help_text': 'The storytelling evaluation of the content'},
            'verdict': {'help_text': 'The final verdict of the review'},
            'publisher': {'help_text': 'The user who published the review'},
            'thumbnail': {'help_text': 'An image related to the review'},
            'timestamp': {'help_text': 'The time the review was created'}
        }

class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'brief_description', 'director', 'producer', 
            'release_date', 'genre', 'industry', 'streaming_platform', 
            'cast', 'timestamp', 'thumbnail'
        ]
        extra_kwargs = {
            'title': {'help_text': 'The title of the movie'},
            'brief_description': {'help_text': 'A brief description of the movie'},
            'director': {'help_text': 'The director of the movie'},
            'producer': {'help_text': 'The producer of the movie'},
            'release_date': {'help_text': 'The release date of the movie'},
            'genre': {'help_text': 'The genre of the movie'},
            'industry': {'help_text': 'The industry (e.g., Hollywood, Bollywood)'},
            'streaming_platform': {'help_text': 'The streaming platform where the movie is available'},
            'cast': {'help_text': 'The cast of the movie'},
            'thumbnail': {'help_text': 'An image related to the review'},
            'timestamp': {'help_text': 'The time the movie details were created'}
        }

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'content', 'publisher', 'timestamp']
        extra_kwargs = {
            'title': {'help_text': 'The title of the news article'},
            'image': {'help_text': 'An image related to the news article'},
            'content': {'help_text': 'The content of the news article'},
            'publisher': {'help_text': 'The user who published the news article'},
            'timestamp': {'help_text': 'The time the news article was created'}
        }

class AwardSerializer(ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'title', 'image', 'content', 'publisher', 'timestamp']
        extra_kwargs = {
            'title': {'help_text': 'The title of the award'},
            'image': {'help_text': 'An image related to the award'},
            'content': {'help_text': 'The content of the award announcement'},
            'publisher': {'help_text': 'The user who published the award details'},
            'timestamp': {'help_text': 'The time the award details were created'}
        }

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'help_text': 'The name of the genre'}
        }

class IndustrySerializer(ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'help_text': 'The name of the industry'}
        }

class StreamingPlatformSerializer(ModelSerializer):
    class Meta:
        model = StreamingPlatform
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'help_text': 'The name of the streaming platform'}
        }



class ForgotPasswordSerializer(ModelSerializer):
    email_address = EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email_address']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise ValidationError("New passwords do not match.")
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class CustomUserSerializer(ModelSerializer):
    liked_reviews = ReviewSerializer(many=True, read_only=True)
    saved_reviews = ReviewSerializer(many=True, read_only=True)
    liked_new = NewsSerializer(many=True, read_only=True)
    saved_new = NewsSerializer(many=True, read_only=True)
    liked_awards = AwardSerializer(many=True, read_only=True)
    saved_awards = AwardSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email_address', 'username', 'password', 'gender', 
            'country', 'is_active', 'is_staff', 'is_superuser',
            'profile_picture', 'liked_reviews', 'saved_reviews', 
            'liked_new', 'saved_new', 'liked_awards', 'saved_awards'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email_address': {'help_text': 'The user\'s email address'},
            'username': {'help_text': 'The user\'s username'},
            'gender': {'help_text': 'The gender of the user'},
            'country': {'help_text': 'The user\'s country'},
            'is_active': {'help_text': 'Indicates if the user is active'},
            'is_staff': {'help_text': 'Indicates if the user is a staff member'},
            'is_superuser': {'help_text': 'Indicates if the user is a superuser'},
            'profile_picture': {'help_text': 'The user\'s profile picture'},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email_address=validated_data['email_address'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        # Update password if provided
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
# class CustomPasswordResetSerializer(serializers.Serializer):
#     email_address = serializers.EmailField()

#     def validate_email_address(self, value):
#         try:
#             self.user = CustomUser.objects.get(email_address=value)
#         except CustomUser.DoesNotExist:
#             raise serializers.ValidationError(_("User with this email does not exist."))
#         return value

#     def save(self):
#         # Generate a token
#         token = default_token_generator.make_token(self.user)
        
#         # Normally, you would save the token in a model or send it to the user via email
#         # Here, we assume your signals.py handles sending the email with the token

#         return token