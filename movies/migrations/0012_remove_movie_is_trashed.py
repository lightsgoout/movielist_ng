# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_auto_20150405_0545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='is_trashed',
        ),
    ]
