from django.core.management import BaseCommand
from movies.models import Person


class Command(BaseCommand):

    def handle(self, *args, **options):
        for person in Person.objects.all():
            person.update_sort_power()
            print u'{} sort power: {}'.format(person, person.sort_power)
