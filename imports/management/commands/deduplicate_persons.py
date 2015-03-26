from django.core.management import BaseCommand
from common.sql_utils import raw_fetch_list
from movies.models import Person


class Command(BaseCommand):

    def handle(self, *args, **options):

        duplicate_ids = raw_fetch_list('select distinct p.kinopoisk_id from movies_person p inner join movies_person p2 on (p2.kinopoisk_id = p.kinopoisk_id and p2.id <> p.id)')

        for duplicate_id in duplicate_ids:
            persons = Person.objects.filter(kinopoisk_id=duplicate_id).order_by('id')

            print u'----'
            print u'Select correct translation:'
            i = 0
            for index, person in enumerate(list(persons)):
                i = index + 1
                print u'{}) {} | {}'.format(index+1, person.name_en, person.name_ru)
            print u'{}) None'.format(i+1)

            choice = raw_input(u'Enter your choice: ')
            choice = int(choice)

            for index, person in enumerate(list(persons)):
                if index + 1 != choice:
                    person.kinopoisk_id = None
                    person.birth_year = None
                    person.name_ru = ''
                    person.save(update_fields=('kinopoisk_id', 'birth_year', 'name_ru'))
