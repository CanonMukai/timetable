from django.db import models
import json

class Make(models.Model):
    file = models.FileField('ファイル')

    def __str__(self):
        return self.file.url

class TimeTable(models.Model):
    school_id = models.IntegerField(unique=True, default=0)
    file_name = models.CharField(max_length=70)
    table = models.TextField(null=True)
    lunch_after = models.IntegerField(null=True)
    cell_list = models.TextField(null=True)
    teacher_list = models.TextField(null=True)
    class_list = models.TextField(null=True)
    jugyo_dict = models.TextField(null=True)
    weekly = models.IntegerField(null=True)

    gen_dict = models.TextField(default=json.dumps({}))
    """
    gen_dict = {'0': '月1', '1': '月2', '2': '月3', '3': '火1', ... }
    """

    convenience = models.TextField(default=json.dumps({}))
    """
    {'鈴木': [0, 1, 2], '佐藤': [3, 4]}
    """

    renzoku_ID = models.TextField(default=json.dumps([]))
    con4_display = models.TextField(default=json.dumps({}))
    """
    {'0,9 1,10 2,11': '国語（1A）と国語（1B）', '3,4 5,6': '英語（1A）'}
    """

    steps = models.IntegerField(default=1000)
    reads = models.IntegerField(default=10)
    class_table_list = models.TextField(null=True)
    class_table_list_for_display = models.TextField(null=True)
    teacher_table_list = models.TextField(null=True)
    days = models.TextField(null=True)
    koma_data_list = models.TextField(null=True)