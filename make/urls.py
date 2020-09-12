from django.urls import path
from . import views

app_name = 'make'

urlpatterns = [
    path('make/', views.make, name='make'),
]