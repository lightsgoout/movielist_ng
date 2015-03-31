# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='arg_score',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
            preserve_default=True,
        ),
    ]
