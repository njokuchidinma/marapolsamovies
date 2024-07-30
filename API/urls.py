from django.urls import path
from .views import ReviewDataHandler, UserProfile,  MovieDataHandler, NewsDataHandler, AwardDataHandler, GenreDataHandler, IndustryDataHandler, StreamingPlatformDataHandler
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('reviews/', ReviewDataHandler.as_view(), name='review_data_handler'),
    path('user/profile/', UserProfile.as_view(), name='user_profile'),
    path('movies/', MovieDataHandler.as_view(), name='movie_data_handler'),
    path('news/', NewsDataHandler.as_view(), name='news_data_handler'),
    path('awards/', AwardDataHandler.as_view(), name='award_data_handler'),
    path('genres/', GenreDataHandler.as_view(), name='genre_data_handler'),
    path('industries/', IndustryDataHandler.as_view(), name='industry_data_handler'),
    path('streaming-platforms/', StreamingPlatformDataHandler.as_view(), name='streaming_platform_data_handler'),
    path('authenticate-user/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-authentication/', TokenRefreshView.as_view(), name='token_refresh'),

]