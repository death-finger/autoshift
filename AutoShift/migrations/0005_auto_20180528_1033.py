# Generated by Django 2.0.5 on 2018-05-28 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoShift', '0004_remove_workhours_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shifts',
            name='offduty',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='shifts',
            name='onduty',
            field=models.CharField(max_length=5),
        ),
    ]