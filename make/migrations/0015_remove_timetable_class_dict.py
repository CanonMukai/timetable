# Generated by Django 2.2.7 on 2020-10-21 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('make', '0014_timetable_class_dict'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='class_dict',
        ),
    ]
