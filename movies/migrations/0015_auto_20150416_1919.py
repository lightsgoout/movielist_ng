# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0014_auto_20150408_0557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertomovie',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
            preserve_default=True,
        ),
    ]
