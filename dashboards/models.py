from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Scripts(models.Model):
    #common
    title = models.CharField(max_length = 255)
    script_type = models.CharField(max_length = 255)
    script = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    #feature film
    script_genre = models.CharField(max_length = 255, blank = True)
    #video short
    platfrom = models.CharField(max_length = 255, blank = True)

    
    

    def __str__(self) -> str:
        return self.user.username

