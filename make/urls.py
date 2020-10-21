from django.urls import path
from . import views

app_name = 'make'

urlpatterns = [
    path('', views.top, name='top'),
    path('make/', views.make, name='make'),
    path('make/constraint/', views.constraint, name='constraint'),
    path('make/success', views.success, name='success'),
    path('make/success/<int:table_id>', views.each_table, name='each'),
    path('make/success/<int:table_id>/download', views.download, name='download'),
]