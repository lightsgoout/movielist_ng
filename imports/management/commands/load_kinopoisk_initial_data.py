import json
import logging
from django.core.management import BaseCommand
from movies.models import Movie


log = logging.getLogger('imports')


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('imports/static_data/kinopoisk_movies_data.json') as f_json:
            data = json.load(f_json)
            for movie_data in data:
                upd = Movie.objects.\
                    filter(imdb_id=movie_data['imdb_id']).\
                    update(title_ru=movie_data['title_ru'] or '',
                           kinopoisk_id=movie_data['kinopoisk_id'])
                if upd:
                    log.info(u'Updated {imdb_id}: {title_ru}'.format(**movie_data))
