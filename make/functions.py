import openpyxl
import json
import numpy as np
import neal

def CellList(excel_file, sheet_num=0):
    """
    入力：エクセルファイルのpath
    出力：[[ID, NAME, CLASS, TEACHER, PLACE], 
          [ID, NAME, CLASS, TEACHER, PLACE],
             ... 
          [ID, NAME, CLASS, TEACHER, PLACE]]
    """
    def get_sheet(excel_file):
        wb = openpyxl.load_workbook(excel_file)
        sheet_name = wb.sheetnames[sheet_num]
        return wb[sheet_name]
    sheet = get_sheet(excel_file)
    cell_list = list(sheet.values)
    return cell_list[1:]

def ClassDict(cell_list):
    """
    入力：cell_list
    出力：class_dict = {ID : {'NAME':'J1', 'CLASS':['1A'], 'TEACHER':['a'], 'PLACE':['1A']},
                       ID : {'NAME':'J2', 'CLASS':['1A'], 'TEACHER':['b'], 'PLACE':['1A']},
                            ...
                       ID : {'NAME':'PE3', 'CLASS':['1A','1B'], 'TEACHER':['g'], 'PLACE':['体育館']}}
    """
    class_dict = {}
    total = len(cell_list)
    for i in range(total):
        class_dict[i] = {}
        class_dict[i]['NAME'] = cell_list[i][1]
        if cell_list[i][2]:
            class_dict[i]['CLASS'] = list(cell_list[i][2].split(','))
        else:
            class_dict[i]['CLASS'] = []
        class_dict[i]['TEACHER'] = list(cell_list[i][3].split(','))
        if cell_list[i][4]:
            class_dict[i]['PLACE'] = list(cell_list[i][4].split(','))
        else:
            class_dict[i]['PLACE'] = []
    return class_dict

def Adjacent(class_dict):
    """
    入力：class_dict
    出力：adjacent (隣接、重なってはいけない授業)
    """
    total = len(class_dict) # cell_listには全ての授業の情報が入っているはず
    adjacent = {}
    for i in range(total):
        adjacent[i] = []
        for j in range(total):
            if i != j:
                c1 = class_dict[i]
                c2 = class_dict[j]
                # CLASS or TEACHER or PLACEが同じ(もしくは被ってるものがある)
                if set(c1['CLASS'])&set(c2['CLASS']) or set(c1['TEACHER'])&set(c2['TEACHER']) or set(c1['PLACE'])&set(c2['PLACE']):
                    adjacent[i].append(j)
    return adjacent

def Hamiltonian(class_dict,
                weekly, total,
                adjacent,  # 第1項
                convenience,  # 第3項
                renzoku_koma, renzoku_ID, # 第4項
                table, one_per_day,  # 第5項
                joint,  # 第6項
                gen_list, one_per_gen,   # 第7項
                renzoku_2koma, not_renzoku_ID,  # 第8項
                w1=1.0, w2=1.0, w3=1.0, w4=1.0, w5=1.0, w6=1.0, w7=1.0, w8=1.0  # 重み
                ):
    """
    ハミルトニアンを計算してQUBOとして返す
    q: 1週間のコマの数、つまりweekly
    alpha: 制約の強さ
    """
    constant = 0
    A = np.zeros((total*weekly, total*weekly))
    # 第1項：問題を表す
    for i in range(total):
        for j in adjacent[i]:
            if sorted([i, j]) in joint:
                continue
            for a in range(weekly):
                k1 = weekly * i + a
                k2 = weekly * j + a
                A[k1, k2] += w1
    # 第2項：制約条件（１つの科目に１つのコマしか割り当てない）
    plus2 = 0
    for i in range(total):
        if len(class_dict[i]['CLASS']) > 1:
            plus2 = 0
        else:
            plus2 = 0
        for a in range(weekly):
            k1 = weekly * i + a
            for b in range(weekly):
                k2 = weekly * i + b
                if k1 == k2: # 1次の項は対角成分に入れる
                    A[k1, k2] -= (w2 + plus2)
                else:
                    A[k1, k2] += (w2 + plus2)
    # 第3項：制約条件（教員の都合を反映）
    for con in convenience:
        # convenience：[ID, c, w(>0)]
        i, a, w = con[0], con[1], con[2]
        k = weekly * i + a
        A[k, k] += w*w3  # w > 0 : 避けたい,  w < 0 : 入りたい
        if w < 0:
            constant -= w*w3
    # 第4項：制約条件（2時間続きにしたい授業）
    for IDs in renzoku_ID:
        constant += w4
        for renzoku in renzoku_koma:
            k1 = weekly * IDs[0] + renzoku[0]
            k2 = weekly * IDs[1] + renzoku[1]
            A[k1, k2] -= w4
    # 第5項：制約条件（各科目は1日1コマ）
    for IDs in one_per_day:
        for komas in table:
            for i in IDs:
                for j in IDs:
                    for a in komas:
                        for b in komas:
                            k1 = weekly * i + a
                            k2 = weekly * j + b
                            if k1 != k2:
                                A[k1, k2] += w5
    # 第6項：制約条件（2クラスでの合同授業）
    """
    TODO: 第1項との絡みをどうするか、(同じ先生、同じ場所の科目はそもそも繋ぐようにしている)
    合同にしたい授業はグラフ上でそもそも繋がないか。
    また、3クラス以上で可能なのか
    """
    for IDs in joint:
        constant += w6
        for a in range(weekly):
            k1 = weekly * IDs[0] + a
            k2 = weekly * IDs[1] + a
            A[k1, k2] -= w6
    # 第7項：制約条件（各科目が同じ時間帯に固まらないようにする）
    for IDs in one_per_gen:
        for komas in gen_list:
            for i in IDs:
                for j in IDs:
                    for a in komas:
                        for b in komas:
                            k1 = weekly * i + a
                            k2 = weekly * j + b
                            if k1 != k2:
                                A[k1, k2] += w7
    # 第8項：制約条件（1教員が3コマ連続にならないようにする）
    for ID_list in not_renzoku_ID:
        ID2 = list(itertools.combinations(ID_list, 2))
        for IDs in ID2:
            for koma2 in renzoku_2koma:
                k1 = weekly * IDs[0] + koma2[0]
                k2 = weekly * IDs[1] + koma2[1]
                A[k1, k2] += w8
                
    # dimodソルバー用のQUBO形式に変換
    Q = {}
    for k1 in range(total*weekly):
        for k2 in range(total*weekly):
            if A[k1, k2] != 0:
                Q[(k1, k2)] = A[k1, k2]
    return Q, constant, A

def search(table, koma):
    for i in range(len(table)):
        j = 0
        for t in table[i]:
            if koma == t:
                return i, j
            j += 1
            
def ClassName(class_dict):
    class_name = set()
    for i in range(total):
        for name in class_dict[i]['CLASS']:
            class_name.add(name)
    class_list = list(class_name)
    class_list.sort()
    return class_list

def TeacherName(class_dict):
    total = len(class_dict)
    teacher_name = set()
    for i in range(total):
        for name in class_dict[i]['TEACHER']:
            teacher_name.add(name)
    teacher_list = list(teacher_name)
    teacher_list.sort()
    return teacher_list

def ClassTable(koma_data, class_dict, class_name, table):
    class_table = {}
    for name in class_name:
        # tableの形によるかも
        class_table[name] = [[None] * len(table) for i in range(len(table[0]))]
    total = len(class_dict)
    #for ID in range(total):
    for ID in koma_data:
        x, y = search(table, koma_data[ID])
        for name in class_dict[ID]['CLASS']:
            # ここでx, yをひっくり返している
            class_table[name][y][x] = class_dict[ID]['NAME'] + ',' + ','.join(class_dict[ID]['TEACHER']) + ',' + ','.join(class_dict[ID]['PLACE'])
    return class_table

def TeacherTable(koma_data, class_dict, teacher_name, weekly):
    teacher_table = {}
    for name in teacher_name:
        teacher_table[name] = [[None] * weekly]
    total = len(class_dict)
    #for ID in range(total):
    for ID in koma_data:
        order = koma_data[ID]
        for name in class_dict[ID]['TEACHER']:
            teacher_table[name][0][order] = class_dict[ID]['NAME'] + ',' + ','.join(class_dict[ID]['CLASS'])
    return teacher_table

# --- 時間割を別のExcelファイルに出力 ---
def write_list_2d(sheet, list2d, start_row, start_col):
    """
    2次元配列を'そのまま見たまんま'Excelファイルのセルに書き込む
    入力：sheet, 2次元配列, 左上セルの行, 左上セルの列
    """
    for y, row in enumerate(list2d):
        for x, cell in enumerate(row):
            sheet.cell(row=start_row + y,
                      column=start_col + x,
                      value=list2d[y][x])
            
def MakeExcelFile(output_file, class_dict, koma_data, table, weekly):
    # 書き込みに必要なデータ
    class_name = ClassName(class_dict)
    class_table = ClassTable(koma_data, class_dict, class_name, table)
    teacher_name = TeacherName(class_dict)
    teacher_table = TeacherTable(koma_data, class_dict, teacher_name, weekly)

    # 書き込み用
    wb = openpyxl.Workbook()

    # 曜日、何限目などの体裁を整える
    weekday = ['月', '火', '水', '木', '金', '土']
    gen = [[1], [2], [3], [4], [5], [6], [7], [8], [9]]

    # sheet1
    sheet1 = wb.create_sheet('クラス別の時間割')
    for i in range(len(class_name)):
        # クラス名
        write_list_2d(sheet1, [[class_name[i]]], 1+i*(len(table[0])+2), 1)
        # 曜日
        write_list_2d(sheet1, [weekday[:len(table)]], 1+i*(len(table[0])+2), 2)
        # 何限
        write_list_2d(sheet1, gen[:len(table[0])], 2+i*(len(table[0])+2), 1)
        # 時間割
        write_list_2d(sheet1, class_table[class_name[i]], 2+i*(len(table[0])+2),2)
        i += 1
    # sheet2
    sheet2 = wb.create_sheet('先生別の時間割')
    # 曜日・何限
    allkoma = [[]]
    for i in range(len(table)):
        for j in range(len(table[i])):
            string = weekday[i] + str(gen[j][0])
            allkoma[0].append(string)
    write_list_2d(sheet2, allkoma, 1, 2)
    # 先生の時間割
    for i in range(len(teacher_name)):
        write_list_2d(sheet2, [['先生']], 1, 1)
        # 先生の名前
        write_list_2d(sheet2, [[teacher_name[i]]], 2+i, 1)
        # 時間割
        write_list_2d(sheet2, teacher_table[teacher_name[i]], 2+i, 2)

    wb.save(output_file)

def KomaData(model):
    cell_list = json.loads(model.cell_list)
    class_dict = ClassDict(cell_list)
    total = len(class_dict)
    adjacent = Adjacent(class_dict)
    convenience = []
    renzoku_koma = []
    renzoku_ID = []
    one_per_day = []
    joint = []
    gen_list = []
    one_per_gen = []
    renzoku_2koma = []
    not_renzoku_ID = []
    w1, w2, w3, w4, w5, w6, w7, w8 = 2, 4, 2, 4, 1, 6, 1, 5
    Q, constant, A = Hamiltonian(
        class_dict,
        model.weekly, total, 
        adjacent, 
        convenience, 
        renzoku_koma, renzoku_ID,
        json.loads(model.table), one_per_day,
        joint,
        gen_list, one_per_gen,
        renzoku_2koma, not_renzoku_ID,
        w1=w1, w2=w2, w3=w3, w4=w4, w5=w5, w6=w6, w7=w7, w8=w8)
    solver = neal.SimulatedAnnealingSampler()
    response = solver.sample_qubo(Q, num_sweeps=1000, num_reads=10)
    for sample0, energy0 in response.data(fields=['sample', 'energy']):
        koma_data = {}
        for key, val in sample0.items():
            if val == 1:
                i = key // model.weekly
                a = key % model.weekly
                koma_data[i] = a
    return koma_data