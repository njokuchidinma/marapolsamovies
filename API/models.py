import uuid
from django.db import models
from django.conf import settings
from .managers import CustomUserManager
from django_userforeignkey.models.fields import UserForeignKey
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission


CONTENT = [
    ('TV_SHOW', 'Tv Show'),
    ('MOVIE', 'Movie'),
]

GENDER = [
    ('MALE', 'male'),
    ('FEMALE', 'female'),
    ]

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email_address = models.EmailField(max_length=255, unique=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=13, choices=GENDER, default='FEMALE')
    country = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email_address']

    def __str__(self):
        return self.email_address

    def has_perm(self, perm, obj=None):
        return True
    
    def has_perms(self, perm, obj=None):
        return True
    

    def has_module_perm(self, app_label):
        return app_label
    

    def has_module_perms(self, app_label):
        return app_label


class Review(models.Model):
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=30, choices=CONTENT)
    streaming_platform = models.CharField(max_length=255)
    cast = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    plot = models.TextField(blank=True, null=True)
    acting = models.TextField(blank=True, null=True)
    characters = models.TextField(blank=True, null=True)
    storytelling = models.TextField(blank=True, null=True)
    verdict = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class News(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='news_images/')
    content = models.TextField()
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Award(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='awards_images/')
    content = models.TextField()
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Industry(models.Model):
    name = models.CharField(max_length=255)

class Genre(models.Model):
    name = models.CharField(max_length=255)

class StreamingPlatform(models.Model):
    name = models.CharField(max_length=255)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    brief_description = models.TextField()
    director = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    release_date = models.DateField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    streaming_platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    cast = models.TextField()  