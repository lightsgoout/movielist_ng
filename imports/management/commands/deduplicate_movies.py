from django.core.management import BaseCommand
from common.sql_utils import raw_fetch
from movies.models import Person, Movie


class Command(BaseCommand):
    def handle(self, *args, **options):

        duplicate_titles = raw_fetch(
            """
            SELECT DISTINCT a.title_en, a.year FROM movies_movie as a
            INNER JOIN movies_movie as b on
            (b.title_en = a.title_en and a.id <> b.id and a.year = b.year)
            """
        )

        for title, year in duplicate_titles:
            correct_movies = Movie.objects.filter(year=year, title_en=title, kinopoisk_id__isnull=False)
            suspected_movies = Movie.objects.filter(year=year, title_en=title, kinopoisk_id__isnull=True)
            for movie in suspected_movies:
                for correct_movie in correct_movies:
                    if set(movie.directors.all().values_list('id', flat=True)) == set(correct_movie.directors.all().values_list('id', flat=True)):
                        print u'Deleting {} - {}'.format(movie.title_en, movie.title_ru)
                        movie.delete()
