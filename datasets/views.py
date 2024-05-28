from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.http import FileResponse, Http404
from django.conf import settings
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Dataset, PretrainedModel
from .serializers import DatasetSerializer, ModelSerializer
from .admin import handle_uploaded_zip
from django.http import JsonResponse
from .forms import DatasetAdminForm, PretrainedModelAdminForm
import os

# Function to handle model upload
def upload_model(request):
    if request.method == 'POST' and request.FILES.get('zip_file'):
        form = PretrainedModelAdminForm(request.POST, request.FILES)
        if form.is_valid():
            model_instance = form.save(commit=False)
            zip_file = form.cleaned_data.get('zip_file')
            if zip_file:
                model_instance.directory_path = handle_uploaded_zip(model_instance, zip_file, f'models/{model_instance.name}')
            model_instance.save()
            return redirect('model_list')
        else:
            return render(request, 'models/upload_model.html', {'form': form})
    form = PretrainedModelAdminForm()
    return render(request, 'models/upload_model.html', {'form': form})

# API ViewSet for Datasets
class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    @action(detail=True, methods=['get'])
    def contents(self, request, pk=None):
        dataset = self.get_object()
        file_path = dataset.file.path

        try:
            with open(file_path, 'r') as file:
                data = file.read()
                return Response({'contents': data})
        except IOError:
            return Response({'error': 'Error reading dataset file'}, status=400)

class PretrainedModelViewSet(viewsets.ModelViewSet):
    queryset = PretrainedModel.objects.all()
    serializer_class = ModelSerializer

# Class-based view to list datasets in a web interface
class DatasetListView(ListView):
    model = Dataset
    template_name = 'datasets/dataset_list.html'

class ModelListView(ListView):
    model = PretrainedModel
    template_name = 'models/model_list.html'

def index(request):
    return render(request, 'index.html')

def homepage(request):
    return render(request, 'homepage.html')

@api_view(['GET'])
def serve_dataset_file(request, pk, filename):
    dataset = get_object_or_404(Dataset, pk=pk)
    file_path = os.path.join(dataset.directory_path, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
    else:
        raise Http404("File does not exist")

def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    return render(request, 'datasets/dataset_detail.html', {'dataset': dataset})

def model_list(request):
    context = {'models': PretrainedModel.objects.all()}
    return render(request, 'models/model_list.html', context)

def model_detail(request, pk):
    model = get_object_or_404(PretrainedModel, pk=pk)
    return render(request, 'models/model_detail.html', {'model': model})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def upload_resources(request):
    if request.method == 'POST':
        upload_type = request.POST.get('upload_type')
        file_obj = request.FILES.get('file')

        if upload_type == 'dataset':
            form = DatasetAdminForm(request.POST, request.FILES)
        elif upload_type == 'model':
            form = PretrainedModelAdminForm(request.POST, request.FILES)
        else:
            return Response({'error': 'Invalid upload type'}, status=400)

        if form.is_valid():
            resource = form.save(commit=False)
            resource.file = file_obj  # Ensure the file is assigned (if not already handled by the form)
            resource.save()
            return Response({'message': 'Upload successful', 'file_url': resource.file.url})
        else:
            return Response({'errors': form.errors}, status=400)
    else:
        return render(request, 'upload_dataset.html')

@login_required
def upload_choices(request):
    return render(request, 'upload_choices.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('upload_choices')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def dataset_upload(request):
    if request.method == 'POST':
        form = DatasetAdminForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            zip_file = form.cleaned_data.get('zip_file')
            if zip_file:
                dataset.directory_path = handle_uploaded_zip(dataset, zip_file, f'datasets/{dataset.name}')
            dataset.save()
            messages.success(request, 'Dataset uploaded successfully!')
            return redirect('dataset_list')
        else:
            messages.error(request, 'Failed to upload dataset.')
    else:
        form = DatasetAdminForm()
    return render(request, 'datasets/dataset_upload.html', {'form': form})



@api_view(['POST'])
def predict(request, pk):
    model = get_object_or_404(PretrainedModel, pk=pk)
    text = request.data.get('text', '')
    # Load the model and make a prediction
    # This is a placeholder - implement the actual model loading and prediction logic
    prediction = {"result": "This is where the prediction result will be"}
    return Response(prediction)
from django.shortcuts import get_object_or_404, render
from .models import PretrainedModel
import os

from django.shortcuts import get_object_or_404, render
from .models import PretrainedModel
import os

from django.shortcuts import get_object_or_404, render
from .models import PretrainedModel
import os

def model_usage_instructions(request, pk):
    model = get_object_or_404(PretrainedModel, pk=pk)
    base_url = request.build_absolute_uri('/')[:-1]  # Get the base URL of the API

    # Path to the model directory
    model_directory = model.directory_path
    config_file_path = model.config_file.path

    # Read the content of the config file
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()
    except IOError:
        config_content = "Error reading the config file."

    # Dynamically generate the API connection details
    api_connection_details = f"""
import requests, os

# Set the base URL to the model files
model_url = "{base_url}/media/{model_directory.replace(os.sep, '/')}"

# Example of how to download a specific model file
file_name = 'model.bin'
response = requests.get(model_url + file_name)

if response.status_code == 200:
    with open(file_name, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {{file_name}}")
else:
    print(f"Failed to download {{file_name}}. Status code: {{response.status_code}}")

# Print the current working directory
print("Current working directory:", os.getcwd())
"""

    complete_content = api_connection_details + "\n" + config_content

    return render(request, 'models/model_usage.html', {'model': model, 'code_snippet': complete_content})



from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings
import os
import zipfile
from django.views.static import serve


def serve_model_folder(request, pk):
    model = get_object_or_404(PretrainedModel, pk=pk)
    folder_path = model.directory_path
    if os.path.exists(folder_path):
        response = HttpResponse(content_type='application/zip')
        zip_file = zipfile.ZipFile(response, 'w')

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname)

        zip_file.close()
        response['Content-Disposition'] = f'attachment; filename={model.name}.zip'
        return response
    else:
        raise Http404("Folder does not exist")
    
    
def serve_single_model_file(request, pk, filename):
    model = get_object_or_404(PretrainedModel, pk=pk)
    file_path = os.path.join(model.directory_path, filename)
    if os.path.exists(file_path):
        return serve(request, os.path.basename(file_path), os.path.dirname(file_path))
    else:
        raise Http404("File does not exist")


# views.py

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Dataset

def download_dataset_script(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    base_url = request.build_absolute_uri('/')[:-1]  # Get the base URL

    script_content = f"""
import requests, os

# Set the base URL to the dataset files
base_url = "{base_url}/datasets/"
dataset_id = {dataset.id}
list_files_url = f"{base_url}{{dataset_id}}/list_files/"

# Fetch the list of files
response = requests.get(list_files_url)

if response.status_code == 200:
    file_list = response.json().get('files', [])
    if not file_list:
        print("No files found.")
    else:
        os.makedirs('dataset_folder', exist_ok=True)
        for file_name in file_list:
            file_url = f"{base_url}{{dataset_id}}/files/{{file_name}}"
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                file_path = os.path.join('dataset_folder', file_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as f:
                    f.write(file_response.content)
                print(f"Downloaded {{file_name}}")
            else:
                print(f"Failed to download {{file_name}}. Status code: {{file_response.status_code}}")
else:
    print(f"Failed to get file list. Status code: {{response.status_code}}")

# Print the current working directory
print("Current working directory:", os.getcwd())

# Example usage of the dataset files
# Adjust the following part based on your dataset usage requirements
import pandas as pd

for file_name in file_list:
    file_path = os.path.join('dataset_folder', file_name)
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        print(f"Loaded {{file_name}} with {{len(df)}} records")
    else:
        print(f"File {{file_name}} is not a CSV, skipping...")

# Adjust the dataset usage logic as needed
"""

    response = HttpResponse(script_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=download_dataset_{dataset.id}.py'
    return response



def download_dataset(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    file_path = dataset.zip_file.path  # Use the correct field name here
    try:
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=dataset.zip_file.name)
    except FileNotFoundError:
        raise Http404("File not found")
    


def list_model_files(request, pk):
    model = get_object_or_404(PretrainedModel, pk=pk)
    folder_path = model.directory_path
    if os.path.exists(folder_path):
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), folder_path)
                file_list.append(file_path)
        return JsonResponse({'files': file_list})
    else:
        return JsonResponse({'error': 'Folder does not exist'}, status=404)

def serve_model_file(request, pk, filename):
    model = get_object_or_404(PretrainedModel, pk=pk)
    file_path = os.path.join(model.directory_path, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
    else:
        raise Http404("File does not exist")