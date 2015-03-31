# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0002_event_arg_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.SmallIntegerField(choices=[(0, b'User watched movie'), (1, b'User planned to watch movie'), (2, b'User followed another user'), (3, b'Achievement unlocked'), (4, b'Achievement locked'), (5, b'User scored movie'), (6, b'User following')]),
            preserve_default=True,
        ),
    ]
