# Generated by Django 3.1.7 on 2022-07-16 17:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events2post',
            name='event_id',
            field=models.CharField(default='event63_2022-07-16', max_length=30),
        ),
        migrations.AlterField(
            model_name='events2post',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 19, 17, 22, 1, 890773, tzinfo=utc), verbose_name='event from_date'),
        ),
        migrations.AlterField(
            model_name='events2post',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 19, 17, 22, 1, 890773, tzinfo=utc), verbose_name='event to_date'),
        ),
        migrations.AlterField(
            model_name='eventsnotapprovednew',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 18, 17, 22, 1, 871665, tzinfo=utc), verbose_name='event date_from'),
        ),
        migrations.AlterField(
            model_name='eventsnotapprovednew',
            name='to_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 18, 17, 22, 1, 871686, tzinfo=utc), verbose_name='event to_date'),
        ),
        migrations.AlterField(
            model_name='eventsnotapprovedold',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 18, 17, 22, 1, 890511, tzinfo=utc), verbose_name='event from_date'),
        ),
        migrations.AlterField(
            model_name='eventsnotapprovedold',
            name='to_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 18, 17, 22, 1, 890527, tzinfo=utc), verbose_name='event to_date'),
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=500)),
                ('parameter_name', models.CharField(max_length=500)),
                ('value', models.CharField(max_length=500)),
            ],
        ),
    ]
