# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_person_imdb_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='sort_power',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]
