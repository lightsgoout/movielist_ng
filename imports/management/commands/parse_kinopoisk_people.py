from HTMLParser import HTMLParser
from django.core.management import BaseCommand
from django.db.models import Count
import time
from movies.models import Person
from kinopoisk.person import Person as KinopoiskPerson


class Command(BaseCommand):

    def handle(self, *args, **options):
        top_actors = Person.objects.\
            annotate(num_movies=Count('starred_movies')).\
            filter(name_ru='').\
            order_by('-num_movies')

        for person in top_actors:
            query = person.name_en.encode('windows-1251', 'ignore')
            decoder = HTMLParser()

            try:
                person_list = KinopoiskPerson.objects.search(query)
                guess = person_list[0]
            except IndexError:
                print 'Could not find kinopoisk info for person {}'.format(person.id)
                time.sleep(1)
                continue
            except Exception as e:
                print e
                time.sleep(1)
                continue

            person.name_ru = decoder.unescape(guess.name)
            person.birth_year = guess.year_birth
            person.kinopoisk_id = guess.id
            person.save(update_fields=('name_ru', 'birth_year', 'kinopoisk_id'))
            print u'Updated {}: {}'.format(person.name_en, person.name_ru)
            time.sleep(1)
