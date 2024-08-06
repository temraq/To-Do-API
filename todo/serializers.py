from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task, TaskPermission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'creator', 'created_at', 'updated_at']
        read_only_fields = ['creator', 'created_at', 'updated_at']

class TaskPermissionSerializer(serializers.ModelSerializer):
    task = serializers.SlugRelatedField(slug_field='title', queryset=Task.objects.all())
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = TaskPermission
        fields = ['id', 'task', 'user', 'permission']
