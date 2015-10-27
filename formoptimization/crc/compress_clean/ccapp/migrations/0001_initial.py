# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InputParam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('param_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='paramval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('val', models.CharField(max_length=256)),
                ('param_name', models.ForeignKey(to='ccapp.InputParam')),
            ],
        ),
    ]
