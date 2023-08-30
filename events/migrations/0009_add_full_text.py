# Generated by Django 3.1.7 on 2023-08-01 13:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20230801_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='events2post',
            name='full_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='eventsnotapprovedold',
            name='full_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='eventsnotapprovednew',
            name='full_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]