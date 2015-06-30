# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentmodel',
            name='family',
            field=models.CharField(max_length=128, blank=True, default=''),
        ),
    ]
