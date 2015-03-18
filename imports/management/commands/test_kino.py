from django.core.management import BaseCommand


class Command(BaseCommand):


    def handle(self, *args, **options):
        from kinopoisk.movie import Movie
        from kinopoisk.person import Person
        person_list = Person.objects.search('Bruce Willis')

        import ipdb; ipdb.set_trace()

