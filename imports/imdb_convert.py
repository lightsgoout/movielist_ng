import logging
from bs4 import BeautifulSoup
from django.conf import settings
from mechanize import Browser
from imports.models import ImportListJob
from movies.models import Movie
import time

log = logging.getLogger('imports')


TIMEOUT = getattr(settings, 'IMDB_CONVERT_TIMEOUT', 10)
MAX_PAGE_TRIES = getattr(settings, 'IMDB_MAX_PAGE_TRIES', 5)
REQUEST_INTERVAL = getattr(settings, 'IMDB_REQUEST_INTERVAL', 3)


class IMDBLayoutChanged(Exception):
    pass


def convert(user, imdb_user_id):
    """
    @type user accounts.models.MovielistUser
    """
    job, _ = ImportListJob.objects.get_or_create(
        user=user,
        imdb_id=imdb_user_id,
        finished=False,
    )
    movies_added = 0

    full_url = "http://www.imdb.com/user/{imdb_id}/watchlist?mode=simple&page={page_id}&ref_=wl_nxt&sort=date_added,asc"

    browser = Browser()
    browser.addheaders = [
        ('User-agent', 'Firefox'),
        ('Accept-Language', 'en-us,en;q=0.5'),
    ]
    browser.set_handle_robots(False)
    for i in xrange(1, 500):
        page_url = full_url.format(imdb_id=imdb_user_id, page_id=i)
        page_tries = 0
        while True:
            try:
                log.info(u"Fetching url {}".format(page_url))
                page = browser.open(page_url, timeout=TIMEOUT)
                break
            except Exception as e:
                if page_tries == MAX_PAGE_TRIES:
                    log.error(u'Max retries reached. Aborting job')
                    raise

                log.error(u'Exception: {}. Retrying...'.format(e))
                time.sleep(REQUEST_INTERVAL)
                page_tries += 1

        html = page.read()
        soup = BeautifulSoup(html)

        if 'This list is not public' in html:
            job.finished = True
            job.save(update_fields=('finished',))
            return True

        try:
            total_movies = soup.findAll('span', {"class": "lister-current-last-item"})[0]
        except IndexError:
            raise IMDBLayoutChanged('Could not find span.lister-current-last-item')

        total_movies = int(total_movies.next_element)
        if total_movies == 0:
            job.finished = True
            job.save(update_fields=('finished',))
            return True

        job.progress = int(round(movies_added / float(total_movies) * 100))
        if job.progress > 0:
            job.save(update_fields=('progress',))
        log.info('Progress: {}%'.format(job.progress))

        try:
            table = soup.findAll("div", {"class": "lister-list"})[0]
        except IndexError:
            raise IMDBLayoutChanged('Could not find div.lister-list')

        row_movies = table.findAll('div', {"class": "lister-col-wrapper"})
        if not len(row_movies):
            """
            Finished.
            """
            job.finished = True
            job.save(update_fields=('finished',))
            return True

        for row in row_movies:
            col_title = row.find('div', {"class": "col-title"})
            col_imdb_rating = row.find('div', {"class": "col-imdb-rating"})
            col_user_rating = row.find('div', {"class": "col-user-rating"})

            rating_str = col_imdb_rating.find('strong').attrs['title']
            rating_imdb = float(rating_str.split(' ')[0])
            votes_imdb = int(rating_str.split(' ')[3].replace(',', ''))

            imdb_id = col_user_rating.find('span', {"class": "userRatingValue"}).attrs['data-tconst']
            try:
                score = int(col_user_rating.find('span', {"class": "rate"}).next_element)
            except ValueError:
                score = None

            title_en = col_title.find('a').next_element
            year = col_title.find('span', {"class": "lister-item-year"}).next_element
            year = int(year.replace(')', '').replace('(', ''))

            try:
                movie = Movie.objects.get(imdb_id=imdb_id)
            except Movie.DoesNotExist:
                try:
                    movie = Movie.objects.get(year=year, title_en=title_en)
                except Movie.DoesNotExist:
                    movie = Movie(
                        year=year,
                        title_ru='',
                        title_en=title_en,
                        imdb_id=imdb_id,
                        source=Movie.IMDB,
                        rating_imdb=rating_imdb,
                        votes_imdb=votes_imdb,
                    )
                    # movie.save()
                except Movie.MultipleObjectsReturned:
                    log.error(u'Multiples movies found for year={} and title_en={}'.format(
                        year,
                        title_en
                    ))
                    continue

            user.add_movie(movie, score=score)
            movies_added += 1
            log.info(u'Found movie: {} score={}'.format(movie, score))

        time.sleep(REQUEST_INTERVAL)
