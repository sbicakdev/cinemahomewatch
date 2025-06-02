from django.urls import path
from .views import fetch_cinema_data, get_movie_db_data, movie_list, movie_details

urlpatterns = [
    path("fetch_cinema_data/", fetch_cinema_data, name="fetch_cinema_data"),
    path("movies/", get_movie_db_data, name='movie'),
    path("movies-template", movie_list, name='movies-template'),
    path('movies/details/<int:movie_id>/', movie_details, name='movie_details'),

]