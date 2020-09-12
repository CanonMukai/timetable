from django.urls import path
from . import views

app_name = 'make'

urlpatterns = [
    # path('make/', views.MakeView.as_view(), name='make'),
    path('make/', views.make, name='make'),
]