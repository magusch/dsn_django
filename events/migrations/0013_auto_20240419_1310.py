# Generated by Django 3.1.7 on 2024-04-19 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20230831_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='events2post',
            name='category',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
