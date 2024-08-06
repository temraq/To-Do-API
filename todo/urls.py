from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskPermissionViewSet, RegisterView, LoginView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'permissions', TaskPermissionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
]
