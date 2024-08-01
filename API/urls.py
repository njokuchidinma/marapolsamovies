from django.urls import path
from .views import ToggleLike, ToggleSave, AddComment, UserDashboard, ReviewDataHandler, UserProfile, UserRegistration, CommentDataHandler, MovieDataHandler, NewsDataHandler, AwardDataHandler, GenreDataHandler, IndustryDataHandler, StreamingPlatformDataHandler
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('toggle-like/<str:model_name>/<int:object_id>/', ToggleLike.as_view(), name='toggle-like'),
    path('toggle-save/<str:model_name>/<int:object_id>/', ToggleSave.as_view(), name='toggle-save'),
    path('add-comment/<str:model_name>/<int:object_id>/', AddComment.as_view(), name='add-comment'),
    path('user-dashboard/', UserDashboard.as_view(), name='user-dashboard'),
    path('reviews/', ReviewDataHandler.as_view(), name='review_data_handler'),
    path('reviews/<int:pk>/', ReviewDataHandler.as_view(), name='review_detail'),
    path('user/profile/', UserProfile.as_view(), name='user_profile'),
    path('user/register/', UserRegistration.as_view(), name='user-registration'),
    path('comments/', CommentDataHandler.as_view(), name='comment_data_handler'),
    path('comments/<int:pk>/', CommentDataHandler.as_view(), name='comment_data_handler_detail'),
    path('authenticate-user/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('movies/', MovieDataHandler.as_view(), name='movie_data_handler'),
    path('movies/<int:pk>/', MovieDataHandler.as_view(), name='movie_detail'),
    path('news/', NewsDataHandler.as_view(), name='news_data_handler'),
    path('news/<int:pk>/', NewsDataHandler.as_view(), name='news_detail'),
    path('awards/', AwardDataHandler.as_view(), name='award_data_handler'),
    path('awards/<int:pk>/', AwardDataHandler.as_view(), name='award_detail'),
    path('genres/', GenreDataHandler.as_view(), name='genre_data_handler'),
    path('genres/<int:pk>/', GenreDataHandler.as_view(), name='genre_detail'),
    path('industries/', IndustryDataHandler.as_view(), name='industry_data_handler'),
    path('industries/<int:pk>/', IndustryDataHandler.as_view(), name='industry_detail'),
    path('streaming-platforms/', StreamingPlatformDataHandler.as_view(), name='streaming_platform_data_handler'),
    path('streaming-platforms/<int:pk>/', StreamingPlatformDataHandler.as_view(), name='streaming_platform_detail'),
    path('authenticate-user/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-authentication/', TokenRefreshView.as_view(), name='token_refresh'),
]