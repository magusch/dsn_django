# Generated by Django 3.1.7 on 2024-05-29 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_postingtime_posting_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsnotapprovedproposed',
            name='image_upload',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
        migrations.AddField(
            model_name='events2post',
            name='image_upload',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
    ]
