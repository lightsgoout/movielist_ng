# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_movielistuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielistuser',
            name='username',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$', b'Enter a valid username.', b'invalid')], help_text=b'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name=b'username', db_index=True),
            preserve_default=True,
        ),
    ]
