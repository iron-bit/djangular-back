from rest_framework import status, permissions, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Post, Community
from api.serializers import PostSerializer

from api.serializers import UserRegistrationSerializer, UserProfileSerializer, CommunitySerializer


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

        # Check if the error is due to username or email conflict
        if 'username' in serializer.errors or 'email' in serializer.errors:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user  # The logged-in user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist refresh token
            refresh_token = RefreshToken(request.data["refresh"])
            refresh_token.blacklist()  # Requires the Simple JWT blacklist app

            return Response({"message": "Logged out successfully!"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class GetPostsView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Post created successfully!", "post": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class CommunitiesView(generics.ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [AllowAny]
