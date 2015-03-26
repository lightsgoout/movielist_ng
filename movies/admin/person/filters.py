from django.contrib.admin import SimpleListFilter


class TranslatedFilter(SimpleListFilter):
    title = u'With translation'
    parameter_name = u'with_translation'

    WITH_TRANSLATION = 'with_translation'
    WITHOUT_TRANSLATION = 'without_translation'

    def lookups(self, request, model_admin):
        return (
            (self.WITH_TRANSLATION, 'With translation'),
            (self.WITHOUT_TRANSLATION, 'Without translation'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == self.WITH_TRANSLATION:
            return queryset.with_translation()
        elif value == self.WITHOUT_TRANSLATION:
            return queryset.without_translation()
        else:
            return queryset
