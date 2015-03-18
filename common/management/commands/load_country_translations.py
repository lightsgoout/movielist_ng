import json
import logging
from django.core.management import BaseCommand
from common.models import Country

log = logging.getLogger('imports')


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('common/static_data/country_translations.json') as f_json:
            data = json.load(f_json)
            for country_data in data:
                upd = Country.objects.\
                    filter(name_en=country_data['name_en']).\
                    update(name_ru=country_data['name_ru'])

                if upd:
                    log.info(u'{name_en}: {name_ru}'.format(**country_data))
