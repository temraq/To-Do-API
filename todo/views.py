from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Task, TaskPermission
from .serializers import TaskSerializer, TaskPermissionSerializer, UserSerializer, LoginSerializer
from rest_framework.exceptions import PermissionDenied

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        user = self.request.user
        creator_tasks = Task.objects.filter(creator=user)
        permitted_tasks = Task.objects.filter(permissions__user=user, permissions__permission=TaskPermission.READ)
        return (creator_tasks | permitted_tasks).distinct()

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator != request.user and not TaskPermission.objects.filter(task=task, user=request.user, permission='update').exists():
            raise PermissionDenied('You do not have permission to update this task.')
       # if task.creator != request.user and not TaskPermission.objects.filter(task=task, user=request.user, permission='read').exists():
               # raise PermissionDenied('You do not have permission to read this task, therefore update.')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator != request.user:
            raise PermissionDenied('You do not have permission to delete this task.')
        return super().destroy(request, *args, **kwargs)

class TaskPermissionViewSet(viewsets.ModelViewSet):
    queryset = TaskPermission.objects.all()
    serializer_class = TaskPermissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        task = serializer.validated_data['task']
        if task.creator != self.request.user:
            raise PermissionDenied('Only the creator can assign permissions.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.task.creator != self.request.user:
            raise PermissionDenied('Only the creator can revoke permissions.')
        instance.delete()

    def get_queryset(self):
        return TaskPermission.objects.filter(task__creator=self.request.user)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(username=serializer.validated_data['username'])
            if user.check_password(serializer.validated_data['password']):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)
