from django.core.management import BaseCommand
from movies.models import Movie


class Command(BaseCommand):

    def handle(self, *args, **options):
        for movie in Movie.objects.all():
            movie.save()
