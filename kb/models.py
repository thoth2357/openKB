from django.db import models
from django.contrib.auth.models import AbstractUser

from mdeditor.fields import MDTextField

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = MDTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    keywords = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)  # Added field for tracking views

    
    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 
    
    def __str__(self):
        return self.email