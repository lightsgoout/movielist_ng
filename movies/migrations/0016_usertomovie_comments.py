# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_auto_20150416_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertomovie',
            name='comments',
            field=models.CharField(max_length=140, blank=True),
            preserve_default=True,
        ),
    ]
