# Generated by Django 2.2.7 on 2020-11-22 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make', '0021_timetable_gen_dict'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='pre_fix',
            field=models.TextField(default='[]'),
        ),
    ]
