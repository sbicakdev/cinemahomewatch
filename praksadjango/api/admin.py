from django.contrib import admin
from .models import Cinema, Movie, Showtime

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude')
    search_fields = ('name', 'address')

class ShowtimeInline(admin.TabularInline):
    model = Showtime
    extra = 1

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'cinema', 'showtime')
    list_filter = ('cinema', 'movie')
    search_fields = ('movie__title', 'cinema__name')
    ordering = ('showtime',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration')
    inlines = [ShowtimeInline]
    search_fields = ('title',)
