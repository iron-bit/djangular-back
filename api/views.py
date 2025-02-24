from rest_framework import status, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Post
from api.serializers import CreatePostSerializer

from api.serializers import UserRegistrationSerializer, UserProfileSerializer


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
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
        
class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    permission_classes = [permissions.AllowAny]  # Permite acceso a cualquier usuario

    def perform_create(self, serializer):
        # Asigna el usuario autenticado como autor del post
        serializer.save(author=self.request.user)