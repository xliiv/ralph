# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20150630_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='hostname',
            field=models.CharField(blank=True, null=True, default=None, max_length=255),
        ),
    ]
