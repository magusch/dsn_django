# Generated by Django 3.1.7 on 2023-08-04 16:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0002_testeventplace'),
        ('events', '0010_change_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(default=events.models.random_event_id, max_length=30)),
                ('title', models.CharField(max_length=500)),
                ('post', models.TextField(blank=True, default='')),
                ('full_text', models.TextField(blank=True, default='', null=True)),
                ('image', models.CharField(blank=True, max_length=500, null=True)),
                ('url', models.CharField(blank=True, max_length=500)),
                ('price', models.CharField(blank=True, max_length=150, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('pub_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='published date and time')),
                ('from_date', models.DateTimeField(default=events.models.default_event_date, verbose_name='event from_date')),
                ('to_date', models.DateTimeField(default=events.models.default_event_date, verbose_name='event to_date')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='place.place')),
            ],
        ),
    ]