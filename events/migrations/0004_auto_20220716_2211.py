# Generated by Django 3.1.7 on 2022-07-16 19:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20220716_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events2post',
            name='event_id',
            field=models.CharField(default='event32_2022-07-16', max_length=30),
        ),
        migrations.AlterField(
            model_name='events2post',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 19, 19, 11, 42, 122622, tzinfo=utc), verbose_name='event from_date'),
        ),
        migrations.AlterField(
            model_name='events2post',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 19, 19, 11, 42, 122622, tzinfo=utc), verbose_name='event to_date'),
        ),
        migrations.AlterField(
            model_name='eventsnotapprovednew',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 18, 19, 11, 42, 95049, tzinfo=utc), verbose_name='event date_from'),
        ),
        migrations.AlterField(
            model_name='eventsnotapprovednew',
            name='to_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 18, 19, 11, 42, 95072, tzinfo=utc), verbose_name='event to_date'),
        ),
        migrations.AlterField(
            model_name='eventsnotapprovedold',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 18, 19, 11, 42, 122365, tzinfo=utc), verbose_name='event from_date'),
        ),
        migrations.AlterField(
            model_name='eventsnotapprovedold',
            name='to_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 18, 19, 11, 42, 122380, tzinfo=utc), verbose_name='event to_date'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='commentary',
            field=models.CharField(max_length=500, null=True),
        ),
    ]