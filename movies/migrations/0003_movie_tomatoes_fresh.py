# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20150313_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='tomatoes_fresh',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
