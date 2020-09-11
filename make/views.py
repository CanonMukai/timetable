from django.shortcuts import render
from django.views.generic import TemplateView

class MakeView(TemplateView):
    template_name = 'make/index.html'
