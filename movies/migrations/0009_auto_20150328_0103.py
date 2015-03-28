# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_person_sort_power'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertomovie',
            name='score',
            field=models.DecimalField(decimal_places=1, choices=[(b'1.0', b'1.0'), (b'1.5', b'1.5'), (b'2.0', b'2.0'), (b'2.5', b'2.5'), (b'3.0', b'3.0'), (b'3.5', b'3.5'), (b'4.0', b'4.0'), (b'4.5', b'4.5'), (b'5.0', b'5.0'), (b'5.5', b'5.5'), (b'6.0', b'6.0'), (b'6.5', b'6.5'), (b'7.0', b'7.0'), (b'7.5', b'7.5'), (b'8.0', b'8.0'), (b'8.5', b'8.5'), (b'9.0', b'9.0'), (b'9.5', b'9.5'), (b'10.0', b'10.0')], max_digits=3, blank=True, null=True, db_index=True),
            preserve_default=True,
        ),
    ]
