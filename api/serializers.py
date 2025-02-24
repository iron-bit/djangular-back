from rest_framework import serializers
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

# Create post
class CreatePostSerializer(serializers.ModelSerializer):
    # Campo extra para recibir la lista de IDs de tags
    tags = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Post
        # Incluimos 'aura' si se quiere permitir su asignación, de lo contrario se usa el default
        fields = ['title', 'content', 'attached_picture', 'is_adult', 'community', 'tags']
        read_only_fields = ['user', 'creation_date', 'aura']
    
    def create(self, validated_data):
        # Extraemos la lista de tags del diccionario validado
        tags_data = validated_data.pop('tags', [])
        # Asignamos el usuario a partir del contexto de la petición
        user = self.context['request'].user
        # Creamos el post; el resto de los datos se desempaquetan con **
        post = Post.objects.create(user=user, **validated_data)
        
        # Por cada tag recibido, se crea la relación en la tabla intermedia
        for tag_id in tags_data:
            try:
                tag = Tag.objects.get(id=tag_id)
                PostTag.objects.create(post=post, tag=tag)
            except Tag.DoesNotExist:
                # Se podría optar por lanzar un error de validación o simplemente ignorar el tag inexistente
                continue
        post.save()
        return post
        






#     title = models.CharField(max_length=50, null=False)
#     content = models.TextField(null=False)
#     attached_picture = models.ImageField(upload_to='images/post_picture/', null=True)
#     aura = models.IntegerField(null=False, default=0)
#     is_adult = models.BooleanField(null=False)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     community = models.ForeignKey(Community, on_delete=models.CASCADE)
