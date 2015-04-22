# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0018_auto_20150420_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='slug',
            field=models.SlugField(max_length=105, blank=True),
            preserve_default=True,
        ),
    ]
