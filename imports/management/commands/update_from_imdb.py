from django.core.management import BaseCommand
from imdb import IMDb
from movies.models import Person, Movie, ActorToMovie


def get_person(imdb_person, create_if_missing=False):
    imdb_name = imdb_person.data['name']
    if ',' in imdb_name:
        normal_name = ' '.join(reversed(imdb_name.split(','))).strip()
    else:
        normal_name = imdb_name
    try:
        person = Person.objects.get(name_en=normal_name)
    except Person.DoesNotExist:
        if create_if_missing:
            person = Person.objects.create(name_en=normal_name)
        else:
            person = None
    return person


class Command(BaseCommand):

    def handle(self, *args, **options):
        ia = IMDb()
        movies = Movie.top.imdb().filter(imdb_processed=False)
        for movie in movies:
            imdb_movie = ia.get_movie(movie.imdb_id.replace('tt', ''))

            if 'original music' in imdb_movie.data:
                composers = imdb_movie.data['original music']
                for composer in composers:
                    person = get_person(composer, True)

                    person.imdb_id = composer.personID
                    person.save()

                    movie.composers.add(person)
                    print u'Added composer {} to movie {}'.format(person, movie)
            else:
                print u'No soundtrack for movie {}'.format(movie)

            cast = imdb_movie.data['cast']
            for actor in cast:
                person = get_person(actor)
                if person is None:
                    continue

                person.imdb_id = actor.personID
                person.save()

                _, created = ActorToMovie.objects.get_or_create(person=person, movie=movie)
                if created:
                    print u'Added actor {} to movie {}'.format(person, movie)
                else:
                    print u'Actor {} already added to movie {}'.format(person, movie)

            movie.imdb_processed = True
            movie.save(update_fields=('imdb_processed',))


