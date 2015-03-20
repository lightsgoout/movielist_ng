import json
import logging
from django.core.management import BaseCommand
from movies.models import Genre

log = logging.getLogger('imports')


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('imports/static_data/genre_translations.json') as f_json:
            data = json.load(f_json)
            for genre_data in data:
                upd = Genre.objects.\
                    filter(name_en=genre_data['name_en']).\
                    update(name_ru=genre_data['name_ru'])

                if upd:
                    log.info(u'{name_en}: {name_ru}'.format(**genre_data))
