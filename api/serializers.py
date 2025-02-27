from rest_framework import serializers
from api.models import CustomUser

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
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']


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
        fields = ['id','title', 'content', 'attached_picture', 'is_adult', 'community', 'community_id', 'tag_ids', 'user', 'creation_date', 'aura', 'post_tags']
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

    def updateAura(self, instance, validated_data):
        if 'aura' in validated_data:
            instance.aura = validated_data['aura']
        instance.save()
        return instance