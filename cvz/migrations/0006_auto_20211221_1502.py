# Generated by Django 3.1.7 on 2021-12-21 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carecenter', '0005_auto_20211221_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carecenter',
            name='center_contact',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='carecenter_employee',
            name='phone_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='carecenter_finance',
            name='Electricity_Bills',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='carecenter_finance',
            name='Employee_salaries',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='carecenter_finance',
            name='Revenue',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='carecenter_head',
            name='phone_number',
            field=models.IntegerField(),
        ),
    ]