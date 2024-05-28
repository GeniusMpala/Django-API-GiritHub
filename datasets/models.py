from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    directory_path = models.CharField(max_length=255, blank=True)  # To store the path of the extracted folder
    zip_file = models.FileField(upload_to='datasets/', null=True, blank=True)

    def __str__(self):
        return self.name

class PretrainedModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    directory_path = models.CharField(max_length=255, blank=True)  # To store the path of the extracted folder
    zip_file = models.FileField(upload_to='models/', null=True, blank=True)
    config_file = models.FileField(upload_to='configs/', null=True, blank=True)

    def __str__(self):
        return self.name

