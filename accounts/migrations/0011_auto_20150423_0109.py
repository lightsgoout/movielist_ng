# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20150420_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielistuser',
            name='email',
            field=models.EmailField(max_length=255, unique=True, null=True, verbose_name=b'email address'),
            preserve_default=True,
        ),
    ]
