# Generated by Django 3.1.7 on 2021-12-21 08:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CareCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('center_name', models.CharField(max_length=128)),
                ('storeno', models.CharField(max_length=300)),
                ('Address', models.CharField(max_length=300)),
                ('no_of_doctors', models.CharField(max_length=100)),
                ('no_of_employees', models.CharField(max_length=100)),
                ('Carecenter_document', models.FileField(blank=True, null=True, upload_to='carecenter_documents')),
                ('Carecenter_image', models.ImageField(blank=True, null=True, upload_to='carecenter_image')),
                ('receptionists_name', models.CharField(max_length=100)),
                ('date_registered', models.DateTimeField(default=django.utils.timezone.now)),
                ('center_contact', models.CharField(default='+91', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='CareCenter_Finance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Employee_salaries', models.IntegerField(max_length=128)),
                ('Electricity_Bills', models.IntegerField(max_length=128)),
                ('Revenue', models.IntegerField(max_length=128)),
                ('Additional_Bills', models.FileField(blank=True, null=True, upload_to='carecenter_finance')),
                ('CareCenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carecenter.carecenter')),
            ],
        ),
        migrations.CreateModel(
            name='Carecenter_employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_Name', models.CharField(blank=True, max_length=128)),
                ('Last_Name', models.CharField(blank=True, max_length=128)),
                ('employee_image', models.ImageField(blank=True, null=True, upload_to='employee_pics')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone_number', models.IntegerField(max_length=128)),
                ('email', models.EmailField(max_length=128)),
                ('date_registered', models.DateTimeField(default=django.utils.timezone.now)),
                ('employee_document_1', models.FileField(blank=True, null=True, upload_to='carecenter_employees')),
                ('employee_document_2', models.FileField(blank=True, null=True, upload_to='carecenter_employees')),
                ('CareCenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carecenter.carecenter')),
            ],
        ),
    ]
