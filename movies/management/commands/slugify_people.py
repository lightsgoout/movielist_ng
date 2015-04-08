from django.core.management import BaseCommand
from movies.models import Person


class Command(BaseCommand):

    def handle(self, *args, **options):
        for person in Person.objects.all():
            person.save()
