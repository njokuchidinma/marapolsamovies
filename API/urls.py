from django.urls import path, include
from rest_framework import routers
from .views import ToggleLike, ToggleSave, AddComment, AllUsersView, UserDashboard, ReviewDataHandler, UserProfile, UserRegistration, CommentDataHandler, MovieDataHandler, NewsDataHandler, AwardDataHandler, GenreDataHandler, IndustryDataHandler, StreamingPlatformDataHandler, MostPopularReviewsView, SuggestedReviewsView, UserCommentsView, TrendingReviewsView, LoginView, LogoutView, ForgotPasswordView, ChangePasswordView, SubscribeNewsletterView, CustomTokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register(r'reviews', ReviewDataHandler, basename='review')
router.register(r'users', UserProfile, basename='user')
router.register(r'all-users', AllUsersView, basename='all-users')
# router.register(r'register', UserRegistration, basename='register')
router.register(r'comments', CommentDataHandler, basename='comment')
router.register(r'movies', MovieDataHandler, basename='movie')
router.register(r'news', NewsDataHandler, basename='news')
router.register(r'awards', AwardDataHandler, basename='award')
router.register(r'genres', GenreDataHandler, basename='genre')
router.register(r'industries', IndustryDataHandler, basename='industry')
router.register(r'streaming-platforms', StreamingPlatformDataHandler, basename='streaming-platform')
router.register(r'newsletter-subscriptions', SubscribeNewsletterView, basename='newsletter-subscription')
router.register(r'forgot-password', ForgotPasswordView, basename='forgot-password')
router.register(r'change-password', ChangePasswordView, basename='change-password')



urlpatterns = [
    path('toggle-like/<str:model_name>/<int:object_id>/', ToggleLike.as_view(), name='toggle-like'),
    path('toggle-save/<str:model_name>/<int:object_id>/', ToggleSave.as_view(), name='toggle-save'),
    path('add-comment/<str:model_name>/<int:object_id>/', AddComment.as_view(), name='add-comment'),
    path('user-dashboard/', UserDashboard.as_view(), name='user-dashboard'),
    # path('reviews/', ReviewDataHandler.as_view(), name='review_data_handler'),
    path('reviews/<int:pk>/', ReviewDataHandler.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='review_detail'),
    # path('users/', AllUsersView.as_view(), name='all-users'),
    # path('user/profile/', UserProfile.as_view(), name='user_profile'),
    path('register/', UserRegistration.as_view(), name='user-registration'),
    # path('comments/', CommentDataHandler.as_view(), name='comment_data_handler'),
    path('comments/<int:pk>/', CommentDataHandler.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='comment_data_handler_detail'),
    # path('movies/', MovieDataHandler.as_view(), name='movie_data_handler'),
    path('movies/<int:pk>/', MovieDataHandler.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='movie_detail'),
    # path('news/', NewsDataHandler.as_view(), name='news_data_handler'),
    path('news/<int:pk>/', NewsDataHandler.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='news_detail'),
    # path('awards/', AwardDataHandler.as_view(), name='award_data_handler'),
    path('awards/<int:pk>/', AwardDataHandler.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='award_detail'),
    # path('genres/', GenreDataHandler.as_view(), name='genre_data_handler'),
    path('genres/<int:pk>/', GenreDataHandler.as_view({'get': 'retrieve', 'post': 'create'}), name='genre_detail'),
    # path('industries/', IndustryDataHandler.as_view(), name='industry_data_handler'),
    path('industries/<int:pk>/', IndustryDataHandler.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='industry_detail'),
    # path('streaming-platforms/', StreamingPlatformDataHandler.as_view(), name='streaming_platform_data_handler'),
    path('streaming-platforms/<int:pk>/', StreamingPlatformDataHandler.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='streaming_platform_detail'),
    # path('authenticate-user/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-authentication/', TokenRefreshView.as_view(), name='token_refresh'),
    path('popular-reviews/', MostPopularReviewsView.as_view(), name='popular_reviews'),
    path('suggested-reviews/<uuid:review_id>/', SuggestedReviewsView.as_view(), name='suggested_reviews'),
    path('user-comments/<str:content_type>/<int:object_id>/', UserCommentsView.as_view(), name='user_comments'),
    path('trending-reviews/', TrendingReviewsView.as_view(), name='trending_reviews'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view({'post': 'create'}), name='forgot_password'),
    path('change-password/', ChangePasswordView.as_view({'post': 'create'}), name='change_password'),
    path('api/refresh/', CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
    # path('subscribe-newsletter/', SubscribeNewsletterView.as_view(), name='subscribe_newsletter'),
    path('', include(router.urls)),
]