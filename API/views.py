from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review, CustomUser, Movie, News, Award, Genre, Industry, StreamingPlatform
from .serializers import ReviewSerializer, CustomUserSerializer, MovieSerializer, NewsSerializer, AwardSerializer, GenreSerializer, IndustrySerializer, StreamingPlatformSerializer


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

class UserProfile(APIView):
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