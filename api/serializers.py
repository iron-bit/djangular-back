from dataclasses import fields

from rest_framework import serializers
from rest_framework.response import Response

from api.models import CustomUser, Post, Tag, PostTag


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'age', 'profile_picture']

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            age=validated_data.get('age', None),
            profile_picture=validated_data.get('profile_picture', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'age', 'profile_picture']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']

class PostTagSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()

    class Meta:
        model = PostTag
        fields = ['tag']

# Create post
class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    post_tags = PostTagSerializer(source='posttag_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'attached_picture', 'is_adult', 'community', 'tags', 'user', 'creation_date', 'aura', 'post_tags']
        read_only_fields = ['user', 'creation_date', 'aura']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        user = self.context['request'].user
        post = Post.objects.create(user=user, **validated_data)

        for tag in tags_data:
            PostTag.objects.create(post=post, tag=tag)
        post.save()
        return post
