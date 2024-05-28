from rest_framework import serializers
from .models import Dataset, PretrainedModel

# class DatasetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Dataset
#         fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PretrainedModel
        fields = '__all__'

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'description', 'file']  # Ensure 'file' is included
