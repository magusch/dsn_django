# Generated by Django 3.1.7 on 2024-05-12 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20240419_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsnotapprovedold',
            name='category',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
