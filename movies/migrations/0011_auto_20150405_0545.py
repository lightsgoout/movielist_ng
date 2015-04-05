# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_auto_20150402_0233'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['name_en']},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['-sort_power']},
        ),
        migrations.AddField(
            model_name='person',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 5, 5, 45, 12, 704455), auto_now_add=True),
            preserve_default=False,
        ),
    ]
