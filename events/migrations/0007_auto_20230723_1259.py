# Generated by Django 3.1.7 on 2023-07-23 09:59

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0002_testeventplace'),
        ('events', '0006_auto_20230310_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='events2post',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='place.place'),
        ),

    ]