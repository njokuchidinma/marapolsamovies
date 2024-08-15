import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from .managers import CustomUserManager
from django_userforeignkey.models.fields import UserForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission



CONTENT = [
    ('TV_SHOW', 'Tv Show'),
    ('MOVIE', 'Movie'),
]   

CATEGORY = [
    ('BEST SERIES OF 2024', 'Best Series of 2024'),
    ('BINGE-WORTHY SERIES', 'Binge-worthy Series'),
    ('MOST POPULAR NOLLYWOOD SERIES', 'Most Popular Nollywood Series'),
    ('MOST POPULAR HOLLYWOOD SERIES', 'Most Popular Hollywood Series'),
    ('MOST POPULAR SERIES IN NIGERIA 2024', 'Most Popular Series in Nigeria 2024'),
    ('TOP RATED SERIES', 'Top Rated Series'),
    ('TOP ON SERIES NETFLIX', 'Top Series on Netflix'),
    ('TOP ON SERIES PRIME', 'Top Series on Prime'),
    ('TOP ON SERIES SHOWMAX', 'Top Series on Showmax'),
]

GENDER = [
    ('MALE', 'male'),
    ('FEMALE', 'female'),
    ]


class CustomUserManager(BaseUserManager):
    def create_user(self, email_address, username, password=None, **extra_fields):
        if not email_address:
            raise ValueError("The Email Address field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email_address, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_address = models.EmailField(max_length=255, unique=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=13, choices=GENDER, default='FEMALE')
    country = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    liked_reviews = models.ManyToManyField('Review', related_name='users_who_liked', blank=True)
    saved_reviews = models.ManyToManyField('Review', related_name='users_who_saved', blank=True)
    liked_new = models.ManyToManyField('News', related_name='users_who_liked', blank=True)
    saved_new = models.ManyToManyField('News', related_name='users_who_saved', blank=True)
    liked_awards = models.ManyToManyField('Award', related_name='users_who_liked', blank=True)
    saved_awards = models.ManyToManyField('Award', related_name='users_who_saved', blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['username']

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


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.content_object}"

class News(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='news_images/')
    content = models.TextField()
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    liked_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_news_items', blank=True)
    saved_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='saved_news_items', blank=True)

class Award(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='awards_images/')
    content = models.TextField()
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    liked_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_awards_items', blank=True)
    saved_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='saved_awards_items', blank=True)

class Industry(models.Model):
    name = models.CharField(max_length=255)

class Genre(models.Model):
    name = models.CharField(max_length=255)

class StreamingPlatform(models.Model):
    name = models.CharField(max_length=255)

class Review(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=30, choices=CONTENT, null=True) 
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True)
    streaming_platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE, null=True)
    cast = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    plot = models.TextField(blank=True, null=True)
    acting = models.TextField(blank=True, null=True)
    characters = models.TextField(blank=True, null=True)
    storytelling = models.TextField(blank=True, null=True)
    verdict = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    timestamp = models.DateTimeField(default=timezone.now)
    ratings = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(10)], null=True)
    liked_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_reviews_items', blank=True)
    saved_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='saved_reviews_items', blank=True)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    brief_description = models.TextField()
    director = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    release_date = models.DateField()
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    streaming_platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    cast = models.TextField()  
    content = models.CharField(max_length=30, choices=CONTENT, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY, null=True)  
    timestamp = models.DateTimeField(default=timezone.now)

class NewsletterSubscription(models.Model):
    email_address = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    subscribed_on = models.DateTimeField(auto_now_add=True)

