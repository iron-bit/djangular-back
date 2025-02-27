from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserProfileView, LogoutView, GetPostsView, PostCreateView
# from .views import UserRegistrationView, UserProfileView, UpdateAura, LogoutView, GetPostsView, PostCreateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    # Es login practicamente
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # ver info usuario. Hay que mejorarlo. TODO
    path('profile/', UserProfileView.as_view(), name='profile'),
    # Para pedir el nuevo token, lo explicaré en clase.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Para crear un post 
    path('create_post/', PostCreateView.as_view(), name='post'),
    path('posts/', GetPostsView.as_view(), name='posts'),
    # path('aura/<int:post_id>/', UpdateAura.as_view(), name='vote_post'),
]
