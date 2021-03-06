import re
from django.contrib import admin
from common.feature_framework import feature_enabled
from settings.features import SPHINX_SEARCH


def parse_runtime(runtime):
    runtime = runtime.strip()
    hour_minutes = 0
    minutes = 0
    if 'h' in runtime:
        m = re.search('(\d+\s*h)', runtime)
        try:
            hour_minutes = int(m.group(0).replace('h', '').strip()) * 60
        except AttributeError:
            hour_minutes = 0

    if 'm' in runtime:
        m = re.search('(\d+\s*m)', runtime)
        try:
            minutes = int(m.group(0).replace('m', '').strip())
        except AttributeError:
            minutes = 0

    return hour_minutes + minutes


def admincolumn(short_description=None, admin_order_field=None,
                allow_tags=None):
    def decorator(func):
        if short_description is not None:
            func.short_description = short_description
        if admin_order_field is not None:
            func.admin_order_field = admin_order_field
        if allow_tags is not None:
            func.allow_tags = allow_tags
        return func

    return decorator


class SphinxModelAdmin(admin.ModelAdmin):

    def get_search_results(self, request, queryset, search_term):
        if search_term:
            if not feature_enabled(SPHINX_SEARCH):
                return super(SphinxModelAdmin, self).get_search_results(
                    request, queryset, search_term)
            sphinx_queryset = self.model.search.query(search_term)
            doc_ids = [doc.pk for doc in sphinx_queryset]
            queryset = queryset.filter(pk__in=doc_ids)
            return queryset, True
        else:
            return super(SphinxModelAdmin, self).get_search_results(
                request, queryset, search_term
            )


def get_translation_stats():
    from movies.models import Movie, Person
    movies_total = Movie.objects.all().count()
    movies_untranslated = Movie.objects.filter(title_ru='').count()
    movies_translated = movies_total - movies_untranslated
    movies_percentage = float(movies_translated) / float(movies_total) * 100

    person_total = Person.objects.all().count()
    person_untranslated = Person.objects.filter(name_ru='').count()
    person_translated = person_total - person_untranslated
    person_percentage = float(person_translated) / float(person_total) * 100

    return {
        'movies': round(movies_percentage, 2),
        'person': round(person_percentage, 2),
    }
