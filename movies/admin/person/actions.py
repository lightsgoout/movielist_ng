from imports import tasks


def kinopoisk_fetch_person_info(modeladmin, request, queryset):
    for person in queryset:
        tasks.kinopoisk_fetch_person_info.delay(person.id)
