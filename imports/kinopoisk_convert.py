import logging
from bs4 import BeautifulSoup
import datetime
from django.conf import settings
from mechanize import Browser
from common.models import Country
from imports.models import ImportListJob
from movies.models import Movie
from kinopoisk.movie import Movie as KinopoiskMovie
import time
import re

log = logging.getLogger('imports')


TIMEOUT = getattr(settings, 'KINOPOISK_CONVERT_TIMEOUT', 10)
MAX_PAGE_TRIES = getattr(settings, 'KINOPOISK_MAX_PAGE_TRIES', 5)
REQUEST_INTERVAL = getattr(settings, 'KINOPOISK_REQUEST_INTERVAL', 3)


class KinopoiskLayoutChanged(Exception):
    pass


def convert(user, kinopoisk_user_id):
    """
    @type user accounts.models.MovielistUser
    """
    russia = Country.objects.get(iso_code='RU')
    job, _ = ImportListJob.objects.get_or_create(
        user=user,
        kinopoisk_id=kinopoisk_user_id,
        finished=False,
    )
    movies_added = 0
    total_movies = 1

    full_url = "http://www.kinopoisk.ru/user/{kinopoisk_id}/votes/list/ord/date/page/{page_id}/#list"

    browser = Browser()
    browser.addheaders = [('User-agent', 'Firefox')]
    browser.set_handle_robots(False)
    for i in xrange(1, 500):
        page_url = full_url.format(kinopoisk_id=kinopoisk_user_id, page_id=i)
        page_tries = 0
        while True:
            try:
                log.info(u"Fetching url {}".format(page_url))
                page = browser.open(page_url, timeout=TIMEOUT)
                break
            except Exception as e:
                if hasattr(e, 'reason') and e.reason == 'Not Found':
                    """
                    Finished convertion
                    """
                    job.finished = True
                    job.progress = int(round(movies_added / float(total_movies) * 100))
                    job.save(update_fields=('finished', 'progress',))
                    return True

                if page_tries == MAX_PAGE_TRIES:
                    log.error(u'Max retries reached. Aborting job')
                    raise

                log.error(u'Exception: {}. Retrying...'.format(e))
                time.sleep(REQUEST_INTERVAL)
                page_tries += 1

        html = page.read()
        soup = BeautifulSoup(html)

        try:
            total_movies = soup.findAll('div', {"class": "pagesFromTo"})[0]
        except IndexError:
            raise KinopoiskLayoutChanged('Could not find div.pagesFromTo')

        total_movies = int(total_movies.next_element.split(' ')[-1])
        if total_movies == 0:
            job.finished = True
            job.save(update_fields=('finished',))
            return True

        job.progress = int(round(movies_added / float(total_movies) * 100))
        if job.progress > 0:
            job.save(update_fields=('progress',))
        log.info('Progress: {}%'.format(job.progress))

        try:
            table = soup.findAll("div", {"class": "profileFilmsList"})[0]
        except IndexError:
            raise KinopoiskLayoutChanged('Could not find div.profileFilmsList')

        for row in table.findAll('div', {"class": "item"}):
            rus_info = row.find('div', {"class": "nameRus"})
            date_added = row.find('div', {"class": "date"}).next_element
            date_added = datetime.datetime.strptime(date_added, "%d.%m.%Y, %M:%S")
            score = row.find('div', {"class": "vote"}).next_element
            try:
                score = int(score)
            except (ValueError, TypeError):
                score = None

            try:
                movie_href = rus_info.next_element.attrs['href']
            except AttributeError:
                raise KinopoiskLayoutChanged('Could not parse movie href')

            kinopoisk_movie_id = re.search('(\d+)', movie_href).group(1)
            try:
                movie = Movie.objects.get(kinopoisk_id=kinopoisk_movie_id)
            except Movie.DoesNotExist:
                movie_title_ru = rus_info.next_element.next_element
                try:
                    movie_year = re.search('\((\d+)\)', movie_title_ru).group(1)
                except AttributeError:
                    log.warning(u"Skipping {}".format(movie_title_ru))
                    continue

                eng_info = row.find('div', {"class": "nameEng"})
                movie_title_en = eng_info.next_element
                try:
                    movie = Movie.objects.get(year=movie_year, title_en=movie_title_en)
                    movie.kinopoisk_id = kinopoisk_movie_id
                    movie.save(update_fields=('kinopoisk_id',))
                except Movie.DoesNotExist:
                    try:
                        guess = KinopoiskMovie.objects.search(movie_title_ru)[0]
                    except IndexError:
                        log.error(u'Could not find kinopoisk movie for title: {}'.format(movie_title_ru))
                        continue

                    movie = Movie(
                        runtime=guess.runtime,
                        year=guess.year,
                        title_ru=guess.title,
                        title_en=guess.title_original,
                        rating_kinopoisk=round(guess.rating, 1) if guess.rating else None,
                        source=Movie.KINOPOISK,
                        kinopoisk_id=kinopoisk_movie_id,
                    )
                    movie.save()
                    movie.countries.add(*Country.objects.filter(
                        name_ru__in=guess.countries))
                    movie.countries.add(russia)

                except Movie.MultipleObjectsReturned:
                    log.error(u'Multiples movies found for year={} and title_en={}'.format(
                        movie_year,
                        movie_title_en
                    ))
                    continue

            user.add_movie(movie, score=score, created_at=date_added)
            movies_added += 1
            log.info(u'Found movie: {}'.format(movie))

        time.sleep(REQUEST_INTERVAL)
