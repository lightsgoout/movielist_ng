from imports import tasks


def kinopoisk_fetch_movie_info(modeladmin, request, queryset):
    for movie in queryset:
        tasks.kinopoisk_fetch_movie_info.delay(movie.id)
