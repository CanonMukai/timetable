# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import MakeForm
from .models import Make, TimeTable
from .functions import *
import json
import ast

def make(request):
    # ファイルアップロード
    if request.method == 'POST':
        form = MakeForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            # 曜日ごとのコマ数
            mon = int(request.POST['mon'])
            tue = int(request.POST['tue'])
            wed = int(request.POST['wed'])
            thu = int(request.POST['thu'])
            fri = int(request.POST['fri'])
            sat = int(request.POST['sat'])
            shape = [mon, tue,  wed, thu, fri, sat]
            table = []
            weekly = 0
            for koma in shape:
                if koma != 0:
                    table.append([])
                    for i in range(koma):
                        table[-1].append(weekly)
                        weekly += 1
            fname = 'make/files/'+str(request.FILES['file'])
            cell_list = CellList(fname, sheet_num=0)
            class_dict = ClassDict(cell_list)
            teacher = TeacherName(class_dict)
            class_list = ClassName(class_dict)
            if TimeTable.objects.filter(school_id=0).exists():
                t = TimeTable.objects.get(school_id=0)
                t.delete()
            timetable = TimeTable(
                school_id=0, 
                file_name=fname, 
                table=json.dumps(table),
                cell_list=json.dumps(cell_list),
                teacher_list=json.dumps(teacher),
                class_list=json.dumps(class_list),
                weekly=weekly
            )
            timetable.save()
            return HttpResponseRedirect(reverse('make:constraint'))
    else:
        form = MakeForm()
    return render(request, 'make/index.html', {'form': form})

def handle_uploaded_file(f):
    fname = 'make/files/' + f.name
    with open(fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

days = ['月', '火', '水', '木', '金', '土']

def constraint(request):
    t = TimeTable.objects.get(school_id=0)
    teacher = json.loads(t.teacher_list)
    table = json.loads(t.table)
    max_koma = 0
    for komas in table:
        max_koma = max(max_koma, len(komas))
    length = len(table)
    table_dict = {}
    for i in range(max_koma):
        table_dict[i+1] = [""] * length
    i = 0
    for day in table:
        j = 0
        for gen in day:
            table_dict[j + 1][i] = {gen: days[i] + str(j+1)}
            j += 1
        i += 1
    params = {
        'teacher': teacher,
        'days': ['月', '火', '水', '木', '金', '土'][:length],
        'tabledict': table_dict
    }
    if request.method == 'POST':
        if 'add' in request.POST:
            return render(request, 'make/constraint.html', params)
        elif 'make' in request.POST:
            t.steps = int(request.POST['steps'])
            t.reads = int(request.POST['reads'])
            t.save()
            class_table_list = ClassTableList(t)
            t.class_table_list = json.dumps(class_table_list)
            t.save()
            return HttpResponseRedirect(reverse('make:success'))
    else:
        return render(request, 'make/constraint.html', params)

def success(request):
    t = TimeTable.objects.get(school_id=0)
    table = json.loads(t.table)
    length = len(table)
    max_koma = 0
    for komas in table:
        max_koma = max(max_koma, len(komas))
    gens = [i+1 for i in range(max_koma)]
    class_table_list = ast.literal_eval(t.class_table_list)
    new_class_table_list = changed(class_table_list)
    params = {
        'days': ['月', '火', '水', '木', '金', '土'][:length],
        'gens': gens,
        'classes': json.loads(t.class_list),
        'tables': new_class_table_list
    }
    return render(request, 'make/success.html', params)

def changed(class_table_list):
    new_one = []
    for class_table in class_table_list:
        new_one.append({})
        for key, value in class_table.items():
            new_one[-1][key] = {}
            i = 1
            for v in value:
                new_one[-1][key][i] = v
                i += 1
    return new_one