# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_movielistuser_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielistuser',
            name='gender',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
    ]
