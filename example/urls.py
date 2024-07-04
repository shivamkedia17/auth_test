from django.urls import path
from . import views

urlpatterns = [
    path('success', views.success, name='successful'),
    path('list', views.list_files, name='test_list'),
    path('create', views.create_file, name='test_create'),
    path('download', views.download_file, name='test_download'),
    path('delete', views.delete_file, name='test_delete'),
]