# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='iso_code',
            field=models.CharField(max_length=2, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
