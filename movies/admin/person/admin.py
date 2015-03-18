# coding=utf-8
from common.utils import admincolumn, SphinxModelAdmin
from movies.admin.person import actions


class PersonAdmin(SphinxModelAdmin):
    list_display = (
        'name_en',
        'name_ru',
        'birth_date',
        'birth_year',
        'kinopoisk_id',
    )
    search_fields = (
        '=id',
        '=kinopoisk_id',
        'name_en',
        'name_ru',
    )
    ordering = ('id',)

    actions = [
        actions.kinopoisk_fetch_person_info,
    ]
