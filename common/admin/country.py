from django.contrib import admin


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'name_en',
        'name_ru',
        'iso_code',
    )
    search_fields = (
        '=id',
        'name_en',
        'name_ru',
        '=iso_code',
    )
    ordering = ('name_en',)
    list_filter = [
        'iso_code'
    ]
