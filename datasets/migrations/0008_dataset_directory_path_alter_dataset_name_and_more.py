# Generated by Django 4.1 on 2024-05-28 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0007_remove_dataset_directory_path_dataset_zip_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='directory_path',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='zip_file',
            field=models.FileField(blank=True, null=True, upload_to='datasets/'),
        ),
        migrations.AlterField(
            model_name='pretrainedmodel',
            name='config_file',
            field=models.FileField(blank=True, null=True, upload_to='configs/'),
        ),
        migrations.AlterField(
            model_name='pretrainedmodel',
            name='zip_file',
            field=models.FileField(blank=True, null=True, upload_to='models/'),
        ),
    ]
