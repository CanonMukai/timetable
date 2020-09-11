from django.urls import path
from . import views

app_name = 'upload_file'

urlpatterns = [
    # path('upload_file', views.UploadFileView.as_view(), name='upload-file'),
    path('upload_file', views.upload_file, name='upload-file'),
]