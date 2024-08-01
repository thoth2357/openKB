from django.db import models
from mdeditor.fields import MDTextField

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = MDTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    keywords = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.title