# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150315_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielistuser',
            name='date_joined',
            field=models.DateField(default=datetime.date(2015, 3, 27), auto_now_add=True),
            preserve_default=False,
        ),
    ]
