# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import MakeForm
from .models import Make, TimeTable
from .functions import *
import json
import ast

def top(request):
    return render(request, 'make/top.html')

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
            # お昼休みの時間
            lunch_after = int(request.POST['lunch'])
            fname = 'make/files/'+str(request.FILES['file'])
            cell_list = CellList(fname, sheet_num=0)
            class_dict = ClassDict(cell_list)
            teacher_list = TeacherName(class_dict)
            class_list = ClassName(class_dict)
            jugyo_dict = JugyoDict(cell_list)
            if TimeTable.objects.filter(school_id=0).exists():
                t = TimeTable.objects.get(school_id=0)
                t.delete()
            timetable = TimeTable(
                school_id=0, 
                file_name=fname, 
                table=json.dumps(table),
                lunch_after=lunch_after,
                cell_list=json.dumps(cell_list),
                teacher_list=json.dumps(teacher_list),
                class_list=json.dumps(class_list),
                jugyo_dict=json.dumps(jugyo_dict),
                weekly=weekly,
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
    teacher_list = json.loads(t.teacher_list)
    jugyo_dict = ast.literal_eval(t.jugyo_dict)
    table = json.loads(t.table)
    max_koma = 0
    for komas in table:
        max_koma = max(max_koma, len(komas))
    length = len(table)
    table_dict = {}
    gen_dict = {}
    for i in range(max_koma):
        table_dict[i+1] = [""] * length
    i = 0
    for day in table:
        j = 0
        for gen in day:
            table_dict[j + 1][i] = {gen: days[i] + str(j+1)}
            gen_dict[gen] = days[i] + str(j+1)
            j += 1
        i += 1
    params = {
        'teacher': teacher_list,
        'days': ['月', '火', '水', '木', '金', '土'][:length],
        'tabledict': table_dict,
        'jugyo': jugyo_dict,
    }
    if request.method == 'POST':
        post_set = {'add', 'clear', 'clear-all', 'add4'}
        if post_set & set(request.POST):
            # TODO: 戻るボタンを押されたときの挙動 現在追加済みの休むコマが誤って表示される
            # 制約3: 先生の都合の取得
            con = ast.literal_eval(t.convenience)
            if 'add' in request.POST:
                teacher = request.POST['teacher']
                con[teacher] = []
                not_in = True
                for i in range(t.weekly):
                    if str(i) in request.POST:
                        not_in = False
                        con[teacher].append(i)
                if not_in:
                    con.pop(teacher)
            elif 'clear' in request.POST:
                teacher = request.POST['clear']
                if teacher in con: # 戻るボタンを押されたときの対処用if
                    con.pop(teacher)
            elif 'clear-all' in request.POST:
                con.clear()
            t.convenience = json.dumps(con)
            t.save()
            # 各教員の休むコマ
            con3_gen = {}
            for name, gens in con.items():
                con3_gen[name] = ""
                for gen in gens:
                    con3_gen[name] += gen_dict[gen] + " "
            params['con3'] = con3_gen
            # 制約4: 2時間連続にしたいコマ
            return render(request, 'make/constraint.html', params)
        elif 'make' in request.POST:
            t.steps = int(request.POST['steps'])
            t.reads = int(request.POST['reads'])
            # convenienceの中に空リストの先生がいたら削除する
            con = ast.literal_eval(t.convenience)
            delete = []
            for key, value in con.items():
                if not value:
                    delete.append(key)
            for key in delete:
                con.pop(key)
            t.convenience = json.dumps(con)
            t.save()
            # 時間割作成
            cell_list = json.loads(t.cell_list)
            class_dict = ClassDict(cell_list)
            koma_data_list = KomaDataList(t, class_dict)
            t.koma_data_list = json.dumps(koma_data_list)
            class_table_list = ClassTableList(t, class_dict)
            t.class_table_list = json.dumps(class_table_list)
            teacher_table_list = TeacherTableList(t, class_dict)
            t.teacher_table_list = json.dumps(teacher_table_list)
            t.save()
            return HttpResponseRedirect(reverse('make:success'))
    else:
        return render(request, 'make/constraint.html', params)

def success(request):
    if request.method == "GET":
        t = TimeTable.objects.get(school_id=0)
        table = json.loads(t.table)
        length = len(table)
        max_koma = 0
        for komas in table:
            max_koma = max(max_koma, len(komas))
        gens = [i+1 for i in range(max_koma)]
        t.days = json.dumps(['月', '火', '水', '木', '金', '土'][:length])
        class_table_list = ast.literal_eval(t.class_table_list)
        new_class_table_list = changed(class_table_list)
        t.class_table_list_for_display = json.dumps(new_class_table_list)
        t.save()
        params = {
            'candidates': [i + 1 for i in range(len(new_class_table_list))],
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

def each_table(request, table_id):
    t = TimeTable.objects.get(school_id=0)
    class_table_list_for_display = ast.literal_eval(t.class_table_list_for_display)
    days = json.loads(t.days)
    koma_data_list = ast.literal_eval(t.koma_data_list)
    info = koma_data_list[table_id - 1]
    params = {
        'table_id': table_id,
        'table': class_table_list_for_display[table_id - 1],
        'days': days,
        'sum': info['sum'],
        'students': info['students'],
        'teachers': info['teachers'],
        'strict': info['strict'],
    }
    return render(request, 'make/each_table.html', params)

def download(request, table_id):
    t = TimeTable.objects.get(school_id=0)
    # エクセルファイルをダウンロードするための呪文
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="timetable{}.xlsx"'.format(table_id)
    # エクセルファイルの内容をresponseに保存
    MakeExcelFile(t, table_id, response)
    return response