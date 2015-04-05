import logging
from optparse import make_option
import tempfile
import zipfile
from clint.textui import progress
from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction
import requests
from common.models import Country
from common.utils import parse_runtime
from movies.models import Movie, Genre, Person, WriterToMovie, WriterRole, \
    ActorToMovie

log = logging.getLogger('imports')

URL = 'http://beforethecode.com/projects/omdb/download.aspx?e={email}&tsv={type}'
CHUNK_SIZE = 1024


def get_value(value):
    try:
        value = unicode(value.replace('N/A', '').strip(), 'latin-1')
    except TypeError:
        value = unicode(value.replace('N/A', '').strip())
    return value or None


def create_m2m(movie, model, relation, raw_data):
    for name in raw_data.split(','):
        name = get_value(name)
        if name:
            instance, _ = model.objects.get_or_create(name_en=name)
            getattr(movie, relation).add(instance)
            log.info(u'\tLinked with {relation}: {value}'.format(
                relation=relation,
                value=name))


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--min-imdb-votes',
            action='store',
            dest='min_imdb_votes',
            default=2000,
            help='Movies with less imdb votes will be skipped',
            type=int,
        ),
        make_option(
            '--file',
            action='store',
            dest='file',
            help='File to load from',
        ),
        make_option(
            '--disable-tomatoes',
            action='store_true',
            dest='disable_tomatoes',
            help='Skip Rotten Tomatoes info',
            default=False,
        ),
        make_option(
            '--disable-main-dump',
            action='store_true',
            dest='disable_main_dump',
            help='Skip main dump',
            default=False,
        )
    )

    def __init__(self):
        super(Command, self).__init__()
        self.existing_movies = set(
            Movie.objects.all().values_list('imdb_id', flat=True)
        )

    def _load_tomatoes_dump(self, dump_f):
        # Skip first line (header)
        for _ in dump_f:
            break

        for line in dump_f:
            (omdb_id, image, rating, meter, reviews, fresh, rotten, consensus,
            user_meter, user_rating, user_reviews, dvd, box_office, production,
            website, last_updated) = line.split('\t')

            image = get_value(image)  # 'fresh' or 'rotten'
            if not image:
                continue

            meter = get_value(meter)
            if not meter:
                continue

            upd = Movie.objects.filter(omdb_id=omdb_id).update(
                rating_tomatoes=get_value(meter),
                tomatoes_fresh=(image in {'fresh', 'certified'}),
            )
            if upd:
                log.info(u'Tomatoes: {} {} ({})'.format(
                    omdb_id,
                    image,
                    meter,
                ))

    def _load_omdb_dump(self, dump_f, min_imdb_votes):
        # Skip first line (header)
        for _ in dump_f:
            break

        for line in dump_f:
            (omdb_id, imdb_id, title_en, year, rated, runtime, genres,
            released, directors, writers, cast, metacritic, imdb_rating,
            imdb_votes, poster, plot_en, full_plot_en, language,
            country, awards, omdb_last_updated) = line.split('\t')

            imdb_id = imdb_id.strip()
            imdb_votes = imdb_votes.replace(',', '')

            if imdb_id in self.existing_movies:
                continue

            # Skip duplicates
            if Movie.objects.filter(
                title_en=get_value(title_en),
                year=get_value(year),
            ).exists():
                log.warning(u'Ignoring {}: duplicate'.format(imdb_id))
                continue

            try:
                imdb_votes = int(get_value(imdb_votes) or 0)
            except ValueError:
                imdb_votes = 0

            if imdb_votes < min_imdb_votes:
                log.info(u'Ignoring {}: less than {} votes'.format(
                    imdb_id, min_imdb_votes))
                continue

            if 'Short' in genres or 'Documentary' in genres:
                log.info(u'Ignoring {}: short or documentary'.format(
                    imdb_id))
                continue

            with transaction.atomic():
                movie = Movie()
                movie.omdb_id = omdb_id
                movie.imdb_id = imdb_id
                movie.title_en = get_value(title_en)
                movie.year = get_value(year)
                movie.rated = get_value(rated) or ''
                movie.runtime = parse_runtime(runtime)
                movie.date_released = get_value(released)
                movie.rating_metacritic = get_value(metacritic)
                movie.rating_imdb = get_value(imdb_rating)
                movie.votes_imdb = imdb_votes
                movie.image_imdb = get_value(poster) or ''
                movie.plot_en = get_value(plot_en) or ''
                movie.full_plot_en = get_value(full_plot_en) or ''
                movie.source_last_updated_at = get_value(omdb_last_updated)
                movie.source = Movie.OMDB
                movie.save()

                self.existing_movies.add(imdb_id)
                log.info(u'New movie: {repr}'.format(repr=movie))

                create_m2m(movie, Person, 'directors', directors)
                create_m2m(movie, Genre, 'genres', genres)
                create_m2m(movie, Country, 'countries', country)

                writers = list(set([w.strip() for w in writers.split(',')]))
                for name in writers:
                    name = get_value(name)
                    if name:
                        writer_role = None
                        person_name = name
                        if '(' in name:
                            if not name.endswith(")"):
                                name += ")"
                            role_name = name[name.index("(") + 1:name.rindex(")")].strip()
                            writer_role, _ = WriterRole.objects.get_or_create(
                                name_en=role_name)
                            person_name = name[0:name.index("(")].strip()

                        person, _ = Person.objects.get_or_create(name_en=person_name)
                        WriterToMovie.objects.create(
                            movie=movie,
                            person=person,
                            role=writer_role,
                        )
                        log.info(u'\tLinked with writer: {name} ({role})'.format(
                            name=person_name, role=writer_role))

                cast = list(set([c.strip() for c in cast.split(',')]))
                for name in cast:
                    name = get_value(name)
                    if name:
                        person, _ = Person.objects.get_or_create(
                            name_en=name)
                        ActorToMovie.objects.create(
                            movie=movie,
                            person=person,
                        )
                        log.info(u'\tLinked with actor: {name}'.format(
                            name=name))

    def load_dump(self, file_name, min_imdb_votes, disable_tomatoes, disable_main_dump):
        with zipfile.ZipFile(file_name) as z:
            if not disable_main_dump:
                with z.open('omdb.txt') as dump_f:
                    self._load_omdb_dump(dump_f, min_imdb_votes)
            if not disable_tomatoes:
                with z.open('tomatoes.txt') as dump_f:
                    self._load_tomatoes_dump(dump_f)

    def handle(self, *args, **options):
        if options['file']:
            self.load_dump(
                options['file'],
                options['min_imdb_votes'],
                options['disable_tomatoes'],
                options['disable_main_dump'],
            )
        else:
            response = requests.get(
                URL.format(email=settings.OMDB_LOGIN, type='movies'),
                stream=True,
            )
            with tempfile.NamedTemporaryFile() as tmp:
                total_length = int(response.headers.get('content-length'))
                for chunk in progress.bar(
                    response.iter_content(chunk_size=CHUNK_SIZE),
                    expected_size=(total_length/CHUNK_SIZE) + 1,
                    label='Downloading OMDB dump '
                ):
                    if chunk:
                        tmp.write(chunk)
                        tmp.flush()
                self.load_dump(
                    tmp.name,
                    options['min_imdb_votes'],
                    options['disable_tomatoes'],
                    options['disable_main_dump'],
                )
