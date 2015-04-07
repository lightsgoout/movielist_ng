# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20150406_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielistuser',
            name='date_of_birth',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
