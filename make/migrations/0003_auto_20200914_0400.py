# Generated by Django 2.2.7 on 2020-09-13 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('make', '0002_auto_20200914_0321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timetable',
            old_name='class_dict',
            new_name='cell_list',
        ),
    ]