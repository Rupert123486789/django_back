import re
from django.db import models
from django.conf import settings


class Actor(models.Model):
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=100, null=True)
    

class Director(models.Model):
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=100, null=True)
    


class Genre(models.Model):
    name = models.CharField(max_length=100)
    


class Movie(models.Model):    
    title = models.CharField(max_length=100)
    overview = models.CharField(max_length=300)
    release_date = models.CharField(max_length=100)
    popularity = models.FloatField()
    vote_average = models.FloatField()
    poster_path = models.CharField(max_length=300)
    adult = models.BooleanField()
    youtube_key = models.CharField(max_length=100, null=True)
    actors = models.ManyToManyField(Actor, related_name='actor_movies')
    directors = models.ManyToManyField(Director, related_name='director_movies')
    genres = models.ManyToManyField(Genre, related_name='genre_movies')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    pick_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='pick_movies')

    


class Movie_Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    rating = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Info(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=100)
