# Generated by Django 2.2.7 on 2020-10-23 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('make', '0017_timetable_jugyo_list'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timetable',
            old_name='jugyo_list',
            new_name='jugyo_dict',
        ),
    ]
