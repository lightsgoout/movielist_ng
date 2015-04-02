# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_auto_20150328_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='sort_power',
            field=models.FloatField(default=0, null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
    ]
