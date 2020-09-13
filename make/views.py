from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import MakeForm
from .models import Make, TimeTable
import json

def make(request):
    # ファイルアップロード
    if request.method == 'POST':
        # 曜日ごとのコマ数
        mon = int(request.POST['mon'])
        tue = int(request.POST['tue'])
        wed = int(request.POST['wed'])
        thu = int(request.POST['thu'])
        fri = int(request.POST['fri'])
        sat = int(request.POST['sat'])
        form = MakeForm(request.POST, request.FILES)
        if TimeTable.objects.filter(school_id=0).exists():
            t = TimeTable.objects.get(school_id=0)
            t.delete()
        timetable = TimeTable(
            school_id=0, 
            file_name=request.FILES['file'], 
            table=json.dumps([mon, tue, wed, thu, fri, sat])
        )
        timetable.save()
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return render(request, 'make/index.html', {'form': form, 'fname': request.FILES['file']})
    else:
        form = MakeForm()
    return render(request, 'make/index.html', {'form': form})

def handle_uploaded_file(f):
    fname = 'make/files/' + f.name
    with open(fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)