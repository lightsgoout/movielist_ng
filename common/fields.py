from django.db import models


RATINGS = (
    ('G', 'G'),
    ('PG', 'PG'),
    ('PG-13', 'PG-13'),
    ('R', 'R'),
    ('NC-17', 'NC-17'),
)


class MovieRatedField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = RATINGS
        kwargs['max_length'] = 5
        super(MovieRatedField, self).__init__(*args, **kwargs)
