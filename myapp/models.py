from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    usericon = models.ImageField(upload_to='media_local/', null=True)


class Contents(models.Model):
    sender = models.CharField(max_length=30)
    receiver = models.CharField(max_length=30)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    id = models.BigAutoField(primary_key=True)
    def __str__(self):
      return str(self.created_at)