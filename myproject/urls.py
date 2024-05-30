from django.contrib import admin
from django.urls import path, include
from datasets import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('models/<int:pk>/predict/', views.predict, name='predict'),
    path('models/<int:pk>/usage/', views.model_usage_instructions, name='model_usage_instructions'),
    path('models/<int:pk>/files/', views.serve_model_folder, name='serve_model_folder'),
    path('models/<int:pk>/files/<str:filename>/', views.serve_single_model_file, name='serve_single_model_file'),
    path('models/<int:pk>/usage/', views.model_usage_instructions, name='model_usage_instructions'),
    path('api/v1/', include('datasets.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', views.homepage, name='homepage'),
    path('datasets/', views.DatasetListView.as_view(), name='dataset_list'),
    path('models/', views.ModelListView.as_view(), name='model_list'),
    path('datasets/<int:dataset_id>/', views.dataset_detail, name='dataset_detail'),
    path('models/upload/', views.upload_model, name='upload_model'),
    path('models/<int:pk>/', views.model_detail, name='model_detail'),
    path('models/<int:pk>/usage/', views.model_usage_instructions, name='model_usage_instructions'),
    path('upload-dataset/', views.upload_resources, name='upload_dataset'),
    path('upload-options/', views.upload_choices, name='upload_choices'),
    path('dataset-upload/', views.dataset_upload, name="dataset_upload"),
    path('upload-model/', views.upload_model, name='upload_model'),
    path('datasets/<int:pk>/download/', views.download_dataset, name='download_dataset'),
    path('datasets/<int:pk>/download_script/', views.download_dataset_script, name='download_dataset_script'),
    path('datasets/<int:pk>/files/<str:filename>/', views.serve_dataset_file, name='serve_dataset_file'),
    path('datasets/<int:pk>/list_files/', views.list_dataset_files, name='list_dataset_files'),
    path('models/<int:pk>/list_files/', views.list_model_files, name='list_model_files'),
    path('models/<int:pk>/files/<str:filename>/', views.serve_model_file, name='serve_model_file'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
