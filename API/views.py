from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review, CustomUser, Comment, Movie, News, Award, Genre, Industry, StreamingPlatform
from .serializers import ReviewSerializer, CustomUserSerializer, CommentSerializer, MovieSerializer, NewsSerializer, AwardSerializer, GenreSerializer, IndustrySerializer, StreamingPlatformSerializer




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

class ReviewDataHandler(APIView):
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


class UserProfile(APIView):
    """ THIS ENDPOINT IS USED TO GET/UPDATE USER INFO ON THE SERVER """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_serializer = self.serializer_class(request.user).data
        return Response({"data": user_serializer}, status=status.HTTP_200_OK)
    

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"data": "ok"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserRegistration(APIView):
    """ Endpoint for user registration """

    def post(self, request):
        """ Register a new user """
        serializer = CustomUserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "User created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDataHandler(APIView):
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
    

class MovieDataHandler(APIView):
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

class NewsDataHandler(APIView):
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

class AwardDataHandler(APIView):
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

class GenreDataHandler(APIView):
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

class IndustryDataHandler(APIView):
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

class StreamingPlatformDataHandler(APIView):
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