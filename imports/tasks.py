from HTMLParser import HTMLParser
import logging
from accounts.models import MovielistUser
from imports.kinopoisk_convert import convert
from movies.celery import app
from movies.models import Movie, Person
from kinopoisk.movie import Movie as KinopoiskMovie
from kinopoisk.person import Person as KinopoiskPerson

log = logging.getLogger('imports')


@app.task()
def kinopoisk_fetch_movie_info(movie_id, *args, **kwargs):
    movie = Movie.objects.get(id=movie_id)

    query = movie.title_en.encode('windows-1251', 'ignore')
    # for html-entity decoding purposes
    decoder = HTMLParser()

    movie_list = KinopoiskMovie.objects.search(query)
    try:
        guess = movie_list[0]
    except IndexError:
        log.error('Could not found kinopoisk info for movie {}'.format(movie_id))
        return

    movie.title_ru = decoder.unescape(guess.title)
    movie.kinopoisk_id = guess.id
    movie.rating_kinopoisk = round(guess.rating, 1) if guess.rating else None
    movie.save(update_fields=('title_ru', 'kinopoisk_id', 'rating_kinopoisk'))


@app.task()
def kinopoisk_fetch_person_info(person_id, *args, **kwargs):
    person = Person.objects.get(id=person_id)

    query = person.name_en.encode('windows-1251', 'ignore')
    decoder = HTMLParser()

    person_list = KinopoiskPerson.objects.search(query)
    try:
        guess = person_list[0]
    except IndexError:
        log.error('Could not found kinopoisk info for person {}'.format(person_id))
        return

    person.name_ru = decoder.unescape(guess.name)
    person.birth_year = guess.year_birth
    person.kinopoisk_id = guess.id
    person.save(update_fields=('name_ru', 'birth_year', 'kinopoisk_id'))


@app.task()
def kinopoisk_import_list(user_id, kinopoisk_id, *args, **kwargs):
    try:
        user = MovielistUser.objects.get(id=user_id)
    except MovielistUser.DoesNotExist:
        log.error('User with id {} does not exist'.format(user_id))
        return

    convert(user, kinopoisk_id)
