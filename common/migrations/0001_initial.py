# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(unique=True, max_length=256)),
                ('name_ru', models.CharField(max_length=256, blank=True)),
                ('iso_code', models.CharField(max_length=2, unique=True, null=True, blank=True)),
            ],
            options={
                'ordering': ('name_en',),
            },
            bases=(models.Model,),
        ),
    ]
