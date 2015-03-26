from ajax_select.fields import AutoCompleteSelectMultipleField, \
    AutoCompleteSelectMultipleWidget
from django.contrib import admin
from django.forms import ModelForm
from movies.models import MovieChain


class MovieChainForm(ModelForm):

    class Meta:
        model = MovieChain
        fields = '__all__'

    # class Media:
    #     css = {
    #         'all': (
    #             "admin/css/overrides.css",
    #         )
    #     }

    movies = AutoCompleteSelectMultipleField(
        'movie',
        required=True,
        help_text=None,
        widget=AutoCompleteSelectMultipleWidget(
            channel='movie',
            attrs={'style': 'width:400px;'}
        ),
    )


class MovieChainAdmin(admin.ModelAdmin):
    form = MovieChainForm

    list_display = (
        'system_name',
        'name_en',
        'is_direct_series',
        'is_suggestable',
    )
