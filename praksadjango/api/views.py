import requests
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cinema, Movie, Showtime, Genre, MoviesGenres
from .forms import ReviewForm
from django.db.models import Avg
import random

# Create your views here.
def fetch_cinema_data(request):
    fetch_url = "https://kinoapi.apps.stroeermb.de/api/cinemas/?latitude=52.50577&longitude=13.4409737&radius=40"

    try:
        response = requests.get(fetch_url)
        response.raise_for_status()
        data = response.json()

        for index, movie_data in enumerate(data.get('movies_tvshows', []), start=1):
            if (index == 30): return JsonResponse({"status": "success", "message": "Fetched all cinema data!"})
            movie_detail_url = "https://kinoapi.apps.stroeermb.de" + movie_data.get('path', '')
            response_movie = requests.get(movie_detail_url)
            response_movie.raise_for_status()
            data_movie = response_movie.json()

            for cinema_data in data_movie.get('cinemas', []):
                cinema, _ = Cinema.objects.get_or_create(
                    cinema_alternative_id=cinema_data.get('id', 0),
                    defaults={
                        'name': cinema_data.get('name', ''),
                        'address': cinema_data.get('address', ''),
                        'latitude': cinema_data.get('latitude', 0),
                        'longitude': cinema_data.get('longitude', 0),
                    }
                )

            movieobj, _ = Movie.objects.get_or_create(
                title=movie_data.get('title', ''),
                defaults={
                    'description': movie_data.get('summary', ''),
                    'duration': movie_data.get('stats', {}).get('duration', 0),
                    'poster_url': movie_data.get('poster_url', ''),
                }
            )

            genres=movie_data.get('genre', [])
            for genre in genres:
                genreobj, _ = Genre.objects.get_or_create(
                    name=genre
                )
                MoviesGenres.objects.get_or_create(
                    movie=movieobj,
                    genre=genreobj
                )

            for showtime_group in data_movie.get('showtimes', []):
                for group_data in showtime_group.get('group_data', []):
                    cinema_id = group_data.get('cinema_id')
                    cinema = Cinema.objects.filter(cinema_alternative_id=cinema_id).first()
                    if not cinema:
                        continue

                    for showtime_info in group_data.get('showtimes_data', []):
                        Showtime.objects.get_or_create(
                            movie=movieobj,
                            cinema=cinema,
                            showtime=showtime_info.get('date_time', '')
                        )

        return JsonResponse({"status": "success", "message": "Fetched all cinema data!"})

    except requests.RequestException as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    

def get_movie_db_data(request):
    try:
        movies = Movie.objects.all().values('title', 'description', 'duration') 

        return JsonResponse({
            "status": "success",
            "movies": list(movies)
        })
    
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

from api.models import Movie, MoviesGenres
import random

import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Movie

@login_required(login_url="/login/")
def movie_list(request):
    user = request.user

    user_genres = [user.favorite_genre_1, user.favorite_genre_2, user.favorite_genre_3]
    user_genres = [g for g in user_genres if g is not None]

    movies = Movie.objects.all()
    all_genres = Genre.objects.all()
    if user_genres:
        top_movies_qs = (
            Movie.objects
            .filter(moviesgenres__genre__in=user_genres)
            .distinct()
            .order_by('-average_rating')[:3]
        )
        recommendations = top_movies_qs
    else:
        recommendations = []

    return render(request, 'movies/movies.html', {
        'movies': movies,
        'all_genres': all_genres,
        'recommendations': recommendations
    })




@login_required(login_url="/login/")
def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie).select_related('cinema')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movie_details', movie_id=movie.id)
    else:
        form = ReviewForm()

    average_rating = movie.average_rating

    reviews = movie.reviews.select_related('user').order_by('-created_at')


    context = {
        'movie': movie,
        'showtimes': showtimes,
        'form': form,
        'average_rating': average_rating,
        'reviews': reviews,
    }
    return render(request, 'movies/movie_details.html', context)
