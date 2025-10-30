from django.db import models
import uuid
from django.conf import settings

# Create your models here.

class Genre(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):

    uu_id = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genres = models.ManyToManyField(Genre)
    length = models.PositiveIntegerField()
    image_card_url = models.URLField(max_length=500, default='')
    image_cover_url = models.URLField(max_length=500, default='')
    video_url = models.URLField(max_length=500, default='')
    movie_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    

class MovieList(models.Model):

    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)