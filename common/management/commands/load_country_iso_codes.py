import json
from django.core.management import BaseCommand
from common.models import Country


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('common/static_data/iso_3166.json') as f:
            json_data = json.load(f)
            for country_data in json_data:
                country_name = country_data['name']
                iso_code = country_data['alpha-2']
                res = Country.objects.\
                    filter(name_en=country_name).\
                    update(iso_code=iso_code)
                if not res:
                    print u'Country {} not found'.format(country_name)

