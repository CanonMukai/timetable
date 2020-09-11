from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import UploadFileForm
from .models import UploadFile

class UploadFileView(TemplateView):
    template_name = 'upload_file/index.html'

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return render(request, 'upload_file/index.html', {'form': form, 'fname': request.FILES['file']})
    else:
        form = UploadFileForm()
    return render(request, 'upload_file/index.html', {'form': form})

def handle_uploaded_file(f):
    fname='upload_file/uploaded_files/'+f.name
    with open(fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)