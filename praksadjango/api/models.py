from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Cinema(models.Model):
    cinema_alternative_id = models.IntegerField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    poster_url = models.TextField(blank=True)
    average_rating = models.FloatField(default=0.0)
    def __str__(self):
        return self.title


class Genre(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class MoviesGenres(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="moviesgenres")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="moviesgenres")

class CustomUser(AbstractUser):
    favorite_genre_1 = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='users_fav1')
    favorite_genre_2 = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='users_fav2')
    favorite_genre_3 = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='users_fav3')

    def __str__(self):
        return self.username

class Review(models.Model):
    rating = models.IntegerField()
    comment = models.CharField(max_length=300)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s review of {self.movie.title} ({self.rating})"

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='showtimes')
    showtime = models.DateTimeField()
    def __str__(self):
        return f"{self.movie.title} at {self.cinema.name} on {self.showtime}"
    



