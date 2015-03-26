from HTMLParser import HTMLParser
from django.core.management import BaseCommand
import time
from movies.models import Movie
from kinopoisk.movie import Movie as KinopoiskMovie


class Command(BaseCommand):

    def handle(self, *args, **options):
        processed_movies = set(
            Movie.objects.\
                filter(kinopoisk_id__isnull=False).\
                values_list('kinopoisk_id', flat=True)
        )

        top_movies = Movie.objects.\
            filter(title_ru='').\
            order_by('-votes_imdb')

        for movie in top_movies:
            query = movie.title_en.encode('windows-1251', 'ignore')
            decoder = HTMLParser()

            try:
                movie_list = KinopoiskMovie.objects.search(query)
                guess = movie_list[0]
            except IndexError:
                print 'Could not find kinopoisk info for movie {}'.format(movie.id)
                time.sleep(1)
                continue
            except Exception as e:
                print e
                time.sleep(1)
                continue

            if int(guess.id in processed_movies):
                print u'Duplicate kinopoisk_id ({}) for movie {}'.format(
                    guess.id, movie.title_en)
                continue

            movie.title_ru = decoder.unescape(guess.title)
            movie.kinopoisk_id = guess.id
            movie.save(update_fields=('title_ru', 'kinopoisk_id'))
            print u'Updated {}: {}'.format(movie.title_en, movie.title_ru)
            time.sleep(1)
            processed_movies.add(int(movie.kinopoisk_id))
