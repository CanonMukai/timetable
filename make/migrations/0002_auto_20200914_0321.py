# Generated by Django 2.2.7 on 2020-09-13 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='class_dict',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='timetable',
            name='teacher_list',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='timetable',
            name='weekly',
            field=models.IntegerField(null=True),
        ),
    ]
