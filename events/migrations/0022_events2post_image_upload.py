# Generated by Django 3.1.7 on 2024-05-29 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_eventsnotapprovedproposed_image_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='events2post',
            name='image_upload',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
    ]