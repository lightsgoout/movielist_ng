from ajax_select.fields import AutoCompleteSelectField, \
    AutoCompleteSelectWidget
from django import forms
from achievements.models import Achievement


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = '__all__'

    condition_movie = AutoCompleteSelectField(
        'movie',
        required=False,
        help_text=None,
        widget=AutoCompleteSelectWidget(
            channel='movie',
            attrs={'style': 'width:400px;'}
        ),
    )

    condition_movie_person = AutoCompleteSelectField(
        'person',
        required=False,
        help_text=None,
        widget=AutoCompleteSelectWidget(
            channel='person',
            attrs={'style': 'width:400px;'}
        ),
    )

    def clean(self):
        cleaned_data = super(AchievementForm, self).clean()

        if (
            cleaned_data['condition_rate_movie_more_than'] or
            cleaned_data['condition_rate_movie_less_than']
        ) and not cleaned_data['condition_movie']:
            raise forms.ValidationError('Movie required for rating criteria.')

        if (
            cleaned_data['condition_rate_movie_more_than'] and
            cleaned_data['condition_rate_movie_less_than']
        ):
            raise forms.ValidationError('Conflicting conditions.')

        if not any((
            cleaned_data['condition_movie_year'],
            cleaned_data['condition_movie_rated'],
            cleaned_data['condition_movie_imdb_rating'],
            cleaned_data['condition_movie_country'],
            cleaned_data['condition_movie_genre'],
            cleaned_data['condition_movie_person'],
        )) and cleaned_data['condition_times']:
            raise forms.ValidationError('Multiplier requires subject.')

        if not any((
            cleaned_data['condition_movie'],
            cleaned_data['condition_movie_year'],
            cleaned_data['condition_movie_imdb_rating'],
            cleaned_data['condition_movie_rated'],
            cleaned_data['condition_movie_country'],
            cleaned_data['condition_movie_genre'],
            cleaned_data['condition_movie_person'],
        )):
            raise forms.ValidationError('Please provide condition.')

        return cleaned_data
