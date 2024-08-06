from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskPermission(models.Model):
    READ = 'read'
    UPDATE = 'update'
    PERMISSION_CHOICES = [
        (READ, 'Read'),
        (UPDATE, 'Update'),
    ]

    task = models.ForeignKey(Task, related_name='permissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='permissions', on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_permission_display()} - {self.task.title}"
