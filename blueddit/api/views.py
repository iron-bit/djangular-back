from django.shortcuts import render
from rest_framework import viewsets

from .models import User, Community, UserInCommunity, Post, Tag, PostTag
from .serializers import UserSerializer, CommunitySerializer, UserInCommunitySerializer, PostSerializer, TagSerializer, PostTagSerializer

# Create your views here.
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
