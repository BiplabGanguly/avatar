from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_timezone = models.CharField(max_length=50, blank=True, default='UTC')
    user_language = models.CharField(max_length=59, default='en')


    def __str__(self):
        return self.user.email