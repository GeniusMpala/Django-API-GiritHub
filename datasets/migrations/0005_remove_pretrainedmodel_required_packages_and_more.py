# Generated by Django 4.1 on 2024-05-25 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0004_remove_dataset_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pretrainedmodel',
            name='required_packages',
        ),
        migrations.AddField(
            model_name='pretrainedmodel',
            name='config_file',
            field=models.FileField(blank=True, null=True, upload_to='models/config/'),
        ),
    ]
