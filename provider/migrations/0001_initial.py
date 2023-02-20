# Generated by Django 3.1.7 on 2021-12-21 08:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carecenter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('First_Name', models.CharField(blank=True, max_length=128)),
                ('Last_Name', models.CharField(blank=True, max_length=128)),
                ('speciality', models.CharField(max_length=300)),
                ('timing', models.TextField(max_length=200)),
                ('ceritificates_of_dr', models.FileField(blank=True, null=True, upload_to='receipts')),
                ('experience', models.CharField(max_length=10)),
                ('about', models.TextField(max_length=1000)),
                ('treatment', models.TextField(max_length=1000)),
                ('fee', models.CharField(max_length=200)),
                ('home_address', models.CharField(max_length=200)),
                ('onn_off', models.BooleanField(default=False)),
                ('CareCenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carecenter.carecenter')),
            ],
        ),
    ]
