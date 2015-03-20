# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20150320_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='imdb_id',
            field=models.CharField(db_index=True, max_length=16, blank=True),
            preserve_default=True,
        ),
    ]
