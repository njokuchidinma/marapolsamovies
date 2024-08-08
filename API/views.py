from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from rest_framework import status, permissions, viewsets, generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .models import Review, CustomUser, Comment, Movie, News, Award, Genre, Industry, StreamingPlatform, NewsletterSubscription
from .permissions import IsAdminOrStaff
from .serializers import ReviewSerializer, CustomUserSerializer, CommentSerializer, MovieSerializer, NewsSerializer, AwardSerializer, GenreSerializer, NewsletterSubscriptionSerializer, IndustrySerializer, StreamingPlatformSerializer, ForgotPasswordSerializer, ChangePasswordSerializer



class LoginView(APIView):
    def post(self, request):
        email_address = request.data.get('email_address')
        password = request.data.get('password')
        
        # Authenticate user
        user = authenticate(request, email_address=email_address, password=password)
        
        if user is not None:
            # Create a refresh token for the authenticated user
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "id": str(user.id),
                "username": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        
        # Return error if authentication fails
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class ToggleLike(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, model_name, object_id):
        model = ContentType.objects.get(model=model_name).model_class()
        obj = get_object_or_404(model, id=object_id)
        if obj.liked_by_users.filter(id=request.user.id).exists():
            obj.liked_by_users.remove(request.user)
            liked = False
        else:
            obj.liked_by_users.add(request.user)
            liked = True
        return Response({'liked': liked}, status=status.HTTP_200_OK)
    
class ToggleSave(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, model_name, object_id):
        model = ContentType.objects.get(model=model_name).model_class()
        obj = get_object_or_404(model, id=object_id)
        if obj.saved_by_users.filter(id=request.user.id).exists():
            obj.saved_by_users.remove(request.user)
            saved = False
        else:
            obj.saved_by_users.add(request.user)
            saved = True
        return Response({'saved': saved}, status=status.HTTP_200_OK) 
    
class AddComment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, model_name, object_id):
        model = ContentType.objects.get(model=model_name).model_class()
        obj = get_object_or_404(model, id=object_id)
        content = request.data.get('content')
        if content:
            comment = Comment.objects.create(
                user=request.user,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                content=content
            )
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

class UserDashboard(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        liked_reviews = request.user.liked_review.all()
        saved_reviews = request.user.saved_review.all()
        liked_news = request.user.liked_news.all()
        saved_news = request.user.saved_news.all()
        liked_awards = request.user.liked_award.all()
        saved_awards = request.user.saved_award.all()
        user_comments = Comment.objects.filter(user=request.user)

        data = {
            'liked_reviews': ReviewSerializer(liked_reviews, many=True).data,
            'saved_reviews': ReviewSerializer(saved_reviews, many=True).data,
            'liked_news': NewsSerializer(liked_news, many=True).data,
            'saved_news': NewsSerializer(saved_news, many=True).data,
            'liked_awards': AwardSerializer(liked_awards, many=True).data,
            'saved_awards': AwardSerializer(saved_awards, many=True).data,
            'user_comments': CommentSerializer(user_comments, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)  

class ReviewDataHandler(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        """ THIS IS THE ENDPOINT CALLS TO GET THE REVIEW DATA FROM THE SERVER """
        
        review_data = self.queryset.all().order_by("-timestamp")
        serializer = self.serializer_class(review_data, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        """ THIS IS THE ENDPOINT THE STAFF SENDS THE REVIEW DATA TO """

        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save(publisher=request.user)
            return Response({"data": "ok"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """ UPDATE REVIEW DATA """
        review = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """ DELETE REVIEW DATA """
        review = get_object_or_404(self.queryset, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class UserProfile(viewsets.ModelViewSet):
#     """ THIS ENDPOINT IS USED TO GET/UPDATE USER INFO ON THE SERVER """

#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         serializer = self.serializer_class(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"data": "ok"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def post(self, request):
#         id = request.data.get('id')
#         if id:

#             try:
#                 user = CustomUser.objects.get(id=id)
#                 serializer = self.serializer_class(user)
#                 return Response({"data": serializer.data}, status=status.HTTP_200_OK)
#             except CustomUser.DoesNotExist:
#                 return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         return Response({"error": "id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    

#     def put(self, request):
#         user = request.user
#         serializer = self.serializer_class(user, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({"data": "ok"}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfile(viewsets.ViewSet):
    """This endpoint is used to get/update user info on the server."""

    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        """Get a specific user's information by user ID (primary key)."""
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(user)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Update a specific user's information."""
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": "User updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """List all users or the current user's information."""
        if request.user.is_authenticated:
            serializer = CustomUserSerializer(request.user)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        """Create a new user."""
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllUsersView(viewsets.ModelViewSet):
    """
    View to retrieve all registered users. Access restricted to admin and staff users.
    """
    permission_classes = [IsAdminOrStaff]  # Use the custom permission
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

class UserRegistration(generics.CreateAPIView):
    """ Endpoint for user registration """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """ Register a new user """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "data": "User created successfully",
                "id": str(user.id),
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDataHandler(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk=None):
        if pk:
            comment = get_object_or_404(Comment, pk=pk)
            serializer = self.serializer_class(comment)
        else:
            comments = self.queryset.all().order_by("-timestamp")
            serializer = self.serializer_class(comments, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"data": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        serializer = self.serializer_class(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserCommentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, content_type, object_id):
        user = request.user
        content_type = ContentType.objects.get(model=content_type)
        comments = Comment.objects.filter(
            content_type=content_type, object_id=object_id, user=user
        )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MovieDataHandler(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        movies = self.queryset.all().order_by("-timestamp")
        serializer = self.serializer_class(movies, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(publisher=request.user)
            return Response({"data": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """ UPDATE MOVIE DATA """
        movie = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """ DELETE MOVIE DATA """
        movie = get_object_or_404(self.queryset, pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NewsDataHandler(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        news = self.queryset.all().order_by("-timestamp")
        serializer = self.serializer_class(news, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(publisher=request.user)
            return Response({"data": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """ UPDATE NEWS DATA """
        news = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(news, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """ DELETE NEWS DATA """
        news = get_object_or_404(self.queryset, pk=pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AwardDataHandler(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        awards = self.queryset.all().order_by("-timestamp")
        serializer = self.serializer_class(awards, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(publisher=request.user)
            return Response({"data": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """ UPDATE AWARD DATA """
        award = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(award, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """ DELETE AWARD DATA """
        award = get_object_or_404(self.queryset, pk=pk)
        award.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GenreDataHandler(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        genres = self.queryset.all()
        serializer = self.serializer_class(genres, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IndustryDataHandler(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        industries = self.queryset.all()
        serializer = self.serializer_class(industries, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """ UPDATE INDUSTRY DATA """
        industry = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(industry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """ DELETE INDUSTRY DATA """
        industry = get_object_or_404(self.queryset, pk=pk)
        industry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamingPlatformDataHandler(viewsets.ModelViewSet):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        platforms = self.queryset.all()
        serializer = self.serializer_class(platforms, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """ UPDATE STREAMING PLATFORM DATA """
        platform = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(platform, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """ DELETE STREAMING PLATFORM DATA """
        platform = get_object_or_404(self.queryset, pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class MostPopularReviewsView(APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request):
        two_months_ago = timezone.now() - timedelta(days=60)
        popular_reviews = Review.objects.annotate(
            interaction_count=Count('liked_by_users') + Count('comments')
        ).filter(timestamp__gte=two_months_ago).order_by('-interaction_count')
        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(popular_reviews, request)
        serializer = ReviewSerializer(popular_reviews, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class SuggestedReviewsView(APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        suggested_reviews = Review.objects.filter(
            genre=review.genre
        ).exclude(id=review.id).order_by('?')
        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(suggested_reviews, request)
        serializer = ReviewSerializer(paginated_reviews, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class TrendingReviewsView(APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request):
        two_days_ago = timezone.now() - timedelta(days=2)
        trending_reviews = Review.objects.annotate(
            interaction_count=Count('liked_by_users') + Count('comments')
        ).filter(timestamp__gte=two_days_ago).order_by('-interaction_count')
        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(trending_reviews, request)
        serializer = ReviewSerializer(paginated_reviews, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class MovieReviewListView(APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request):
        movie_reviews = Review.objects.filter(content='MOVIE')
        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(movie_reviews, request)
        serializer = ReviewSerializer(paginated_reviews, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class TVShowReviewListView(APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request):
        tv_show_reviews = Review.objects.filter(content='TV_SHOW')
        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(tv_show_reviews, request)
        serializer = ReviewSerializer(paginated_reviews, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class SubscribeNewsletterView(viewsets.ModelViewSet):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer

    def post(self, request):
        serializer = NewsletterSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Subscribed to newsletter"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         try:
#             # Blacklist the refresh token
#             refresh_token = request.data.get("refresh")
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Retrieve the refresh token from the request data
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Attempt to blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            # TokenError is raised when a token is invalid or cannot be blacklisted
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch other exceptions and return a more detailed error message
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ForgotPasswordView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ForgotPasswordSerializer
    def post(self, request):
        email = request.data.get('email_address')
        try:
            user = CustomUser.objects.get(email_address=email)
            new_password = CustomUser.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            send_mail(
                'Your new password',
                f'Your new password is: {new_password}',
                'admin@marapolsa.com',
                [email],
            )
            return Response({"message": "New password sent to your email"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordView(viewsets.ModelViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all() 

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "New passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    

class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view to generate an access token with a specific expiration time.
    """
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                # Decode the refresh token to get the user
                access_token = AccessToken()
                access_token.set_exp(lifetime=timedelta(days=3))
                
                # Use the refresh token to create a new access token
                user = access_token.for_user(refresh_token.user)
                access_token['user_id'] = user.id
                
                # Add custom access token to the response
                response.data['access'] = str(access_token)

        return response