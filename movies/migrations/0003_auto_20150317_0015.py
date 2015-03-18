# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_moviechain_is_suggestable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviechain',
            name='is_direct_series',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moviechain',
            name='is_suggestable',
            field=models.BooleanField(default=True, db_index=True),
            preserve_default=True,
        ),
    ]
