# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0019_auto_20150422_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image_mvlst',
            field=models.URLField(max_length=512, blank=True),
            preserve_default=True,
        ),
    ]
