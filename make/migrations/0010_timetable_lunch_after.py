# Generated by Django 2.2.7 on 2020-09-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make', '0009_timetable_convenience'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='lunch_after',
            field=models.IntegerField(null=True),
        ),
    ]
