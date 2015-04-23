import hashlib
from django.conf import settings
from django.core.management import BaseCommand
import requests
import shutil
import time
from movies.models import Movie


class Command(BaseCommand):

    def handle(self, *args, **options):
        unfetched_movies = Movie.objects.filter(image_mvlst='').order_by('id')

        for movie in unfetched_movies:
            if movie.image_imdb:
                r = requests.get(movie.image_imdb, stream=True)
            elif movie.kinopoisk_id:
                r = requests.get(movie.image_kinopoisk, stream=True)
            else:
                continue

            if r.status_code == 200:
                m = hashlib.md5()
                m.update(str(movie.pk) + 'salty salt')
                file_name = '{}.jpg'.format(m.hexdigest())
                full_path = '{}/{}'.format(settings.POSTER_FETCH_DIR, file_name)
                with open(full_path, 'wb') as img:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, img)
                    movie.image_mvlst = settings.POSTER_BASE_URL + file_name
                    movie.save(update_fields=('image_mvlst',))
                    print u'{} OK'.format(movie.image_imdb)
                    time.sleep(0.5)
