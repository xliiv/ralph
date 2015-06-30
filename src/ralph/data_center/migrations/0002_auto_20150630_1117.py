# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_center', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datacenterasset',
            name='slots',
            field=models.FloatField(verbose_name='Slots', max_length=64, default=0, help_text='For blade centers: the number of slots available in this device. For blade devices: the number of slots occupied.'),
        ),
        migrations.AlterField(
            model_name='rackaccessory',
            name='remarks',
            field=models.CharField(verbose_name='Additional remarks', max_length=1024, blank=True),
        ),
    ]
