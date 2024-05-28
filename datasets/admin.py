from django.contrib import admin
from django import forms
from .models import Dataset, PretrainedModel
from .forms import DatasetAdminForm, PretrainedModelAdminForm
import zipfile
import os
from django.conf import settings

def handle_uploaded_zip(instance, zip_file, upload_dir):
    upload_path = os.path.join(settings.MEDIA_ROOT, upload_dir)
    os.makedirs(upload_path, exist_ok=True)
    
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(upload_path)

    return upload_dir

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    form = DatasetAdminForm
    list_display = ('name', 'description', 'directory_path')

    def save_model(self, request, obj, form, change):
        zip_file = form.cleaned_data.get('zip_file', None)
        if zip_file:
            obj.directory_path = handle_uploaded_zip(obj, zip_file, f'datasets/{obj.name}')
        super().save_model(request, obj, form, change)

@admin.register(PretrainedModel)
class PretrainedModelAdmin(admin.ModelAdmin):
    form = PretrainedModelAdminForm
    list_display = ('name', 'description', 'directory_path')

    def save_model(self, request, obj, form, change):
        zip_file = form.cleaned_data.get('zip_file', None)
        if zip_file:
            obj.directory_path = handle_uploaded_zip(obj, zip_file, f'models/{obj.name}')
        super().save_model(request, obj, form, change)
