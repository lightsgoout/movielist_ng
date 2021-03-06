from django.contrib.admin import SimpleListFilter


class ImageFilter(SimpleListFilter):
    title = u'Image status'
    parameter_name = u'image_status'

    WITH_IMAGE = 'with_image'
    WITHOUT_IMAGE = 'without_image'

    def lookups(self, request, model_admin):
        return (
            (self.WITH_IMAGE, 'With image'),
            (self.WITHOUT_IMAGE, 'Without image'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == self.WITH_IMAGE:
            return queryset.with_image()
        elif value == self.WITHOUT_IMAGE:
            return queryset.without_image()
        else:
            return queryset


# TODO: Duplicate code (copypasted from person)
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
