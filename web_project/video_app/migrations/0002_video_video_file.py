# Generated by Django 5.0.4 on 2024-04-19 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_file',
            field=models.FileField(default=1, upload_to='videos/'),
            preserve_default=False,
        ),
    ]
