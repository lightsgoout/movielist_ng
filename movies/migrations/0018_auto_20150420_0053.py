# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0017_auto_20150419_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertomovie',
            name='created_at',
            field=models.DateTimeField(db_index=True),
            preserve_default=True,
        ),
    ]
