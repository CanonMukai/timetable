# Generated by Django 2.2.7 on 2020-11-22 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make', '0022_timetable_pre_fix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='pre_fix',
            field=models.TextField(default='{}'),
        ),
    ]
