from django.contrib import admin
from django.http import HttpRequest
from .models import CustomUser, Review, News, Award, Movie, Industry, Genre, StreamingPlatform, Comment, NewsletterSubscription
from django.shortcuts import get_object_or_404
from django.contrib.auth.admin import UserAdmin




@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser
    
    fieldsets = (
        (None, {"fields": ("email_address", "password")}),
        ("Personal Info", {"fields": ("username", "country", "gender", "profile_picture")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("User Interactions", {'fields': ('liked_reviews', 'saved_reviews', 'liked_new', 'saved_new', 'liked_awards', 'saved_awards')}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email_address", "username", "password1", "password2"),
        }),
    )
    list_display = ("email_address", "username", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active",)
    search_fields = ("email_address", "username")
    ordering = ("email_address",)
    readonly_fields = ("last_login", "date_joined")

    def save_model(self, request, obj, form, change):
        if not change:
            # New user
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request: HttpRequest) -> bool:
        if request.user.is_superuser == True:
            return True
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if request.user.is_superuser == True:
            return True
        return False

    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        if request.user.is_superuser == True:
            return True
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        if request.user.is_superuser == True:
            return True
        return False

    def has_module_permission(self, request: HttpRequest) -> bool:
        if request.user.is_superuser == True:
            return True
        return False

    def current_user(self, request):
        current_user = get_object_or_404(CustomUser, email_address=request.user.email_address)
        return current_user
    
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'streaming_platform', 'director', 'publisher', 'timestamp')
    search_fields = ('title', 'content', 'director', 'cast')
    list_filter = ('content', 'streaming_platform', 'timestamp')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'timestamp')
    search_fields = ('title', 'content')
    list_filter = ('timestamp',)

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'timestamp')
    search_fields = ('title', 'content')
    list_filter = ('timestamp',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'director', 'producer', 'genre', 'streaming_platform', 'industry')
    search_fields = ('title', 'brief_description', 'director', 'producer', 'cast', 'content')
    list_filter = ('release_date', 'genre', 'streaming_platform', 'industry', 'timestamp')

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(StreamingPlatform)
class StreamingPlatformAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'content', 'timestamp', 'like_count')
    search_fields = ('content', 'user__username')
    list_filter = ('timestamp',)

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'first_name', 'subscribed_on')
    search_fields = ('email_address', 'first_name')