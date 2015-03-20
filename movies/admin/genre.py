from django.contrib import admin


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name_en',
        'name_ru',
    )
