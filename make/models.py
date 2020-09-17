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
    cell_list = models.TextField(null=True)
    teacher_list = models.TextField(null=True)
    class_list = models.TextField(null=True)
    weekly = models.IntegerField(null=True)
    convenience = models.TextField(default=json.dumps({}))
    steps = models.IntegerField(default=1000)
    reads = models.IntegerField(default=10)
    class_table_list = models.TextField(null=True)