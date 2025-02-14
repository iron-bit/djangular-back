from rest_framework import serializers

from .models import User, Community, UserInCommunity, Post, Tag, PostTag


#TODO check if userSerialize is needed
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class UserInCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInCommunity
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = '__all__'