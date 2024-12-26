from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class rating(models.Model):
    objects = None
    username=models.CharField(max_length=300)
    cuisine=models.CharField(max_length=300)
    ratings=models.IntegerField(max_length=3)
class content:
    def __init__(self, a):
        self.name = a['cuisine']
        self.images = a['images']