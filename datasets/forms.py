from django import forms
from .models import Dataset, PretrainedModel
from django.core.exceptions import ValidationError
import os

class DatasetAdminForm(forms.ModelForm):
    zip_file = forms.FileField(required=False, help_text="Upload a ZIP file containing the dataset folder.")

    class Meta:
        model = Dataset
        fields = ['name', 'description', 'zip_file']

    def clean_zip_file(self):
        zip_file = self.cleaned_data.get('zip_file', None)
        if zip_file:
            valid_extensions = ['.zip']
            extension = os.path.splitext(zip_file.name)[1].lower()
            if extension not in valid_extensions:
                raise ValidationError("Unsupported file extension.")
        return zip_file

class PretrainedModelAdminForm(forms.ModelForm):
    zip_file = forms.FileField(required=False, help_text="Upload a ZIP file containing the pretrained model folder.")

    class Meta:
        model = PretrainedModel
        fields = ['name', 'description', 'zip_file']

    def clean_zip_file(self):
        zip_file = self.cleaned_data.get('zip_file', None)
        if zip_file:
            valid_extensions = ['.zip']
            extension = os.path.splitext(zip_file.name)[1].lower()
            if extension not in valid_extensions:
                raise ValidationError("Unsupported file extension.")
        return zip_file
