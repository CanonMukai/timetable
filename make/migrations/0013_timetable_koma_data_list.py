# Generated by Django 2.2.7 on 2020-10-19 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make', '0012_timetable_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='koma_data_list',
            field=models.TextField(null=True),
        ),
    ]
