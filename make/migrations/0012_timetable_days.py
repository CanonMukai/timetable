# Generated by Django 2.2.7 on 2020-10-19 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make', '0011_timetable_class_table_list_for_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='days',
            field=models.TextField(null=True),
        ),
    ]