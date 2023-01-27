from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Collection(models.Model):
    title = models.CharField(max_length=100)
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    description=models.CharField(max_length=500)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='collections')
    def __str__(self) -> str:
        return self.title

class Movies(models.Model):
    title = models.CharField(max_length=100)
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    description=models.CharField(max_length=500)
    collection=models.ManyToManyField(Collection,related_name="movies")
    def __str__(self) -> str:
        return self.title

class Genre(models.Model):
    movie=models.ManyToManyField(Movies,related_name="genres")
    genre_name= models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.genre_name

class GenreStats(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    genre_name=models.CharField(max_length=30)
    genre_count=models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.genre_name)+str(self.genre_count)

    class Meta:
        ordering = ['-genre_count']


class RequestCount(models.Model):
    requestCount=models.IntegerField()
    def __str__(self) -> str:
        return self.requestCount