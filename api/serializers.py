from dataclasses import fields

from rest_framework import serializers
from api.models import CustomUser, Tag, PostTag, Community, Post


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", 'username', 'email', 'password', 'age', 'profile_picture']

    def validate(self, data):
        """Check if the username or email already exists."""
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})

        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        return data

    def create(self, validated_data):
        user = CustomUser(
            first_name=validated_data['first_name'],
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
        fields = '__all__'


class PostTagSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()

    class Meta:
        model = PostTag
        fields = ['tag']


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'community_picture', 'is_adult']


# Create post
class PostSerializer(serializers.ModelSerializer):
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    user = serializers.StringRelatedField()
    post_tags = PostTagSerializer(source='posttag_set', many=True, read_only=True)
    community_id = serializers.IntegerField(write_only=True)
    community = CommunitySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'attached_picture', 'is_adult', 'community', 'community_id', 'tag_ids',
                  'user', 'creation_date', 'aura', 'post_tags']
        read_only_fields = ['user', 'creation_date']

    def create(self, validated_data):
        tags = validated_data.pop('tag_ids', [])
        community_id = validated_data.pop('community_id')
        user = self.context['request'].user
        community = Community.objects.get(id=community_id)
        post = Post.objects.create(user=user, community=community, **validated_data)

        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            PostTag.objects.create(post=post, tag=tag)
        post.save()
        return post