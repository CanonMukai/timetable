# Generated by Django 2.2.7 on 2020-09-15 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make', '0003_auto_20200914_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='class_list',
            field=models.TextField(null=True),
        ),
    ]
