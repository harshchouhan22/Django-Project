# Generated by Django 3.1.7 on 2021-12-21 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carecenter', '0004_carecenter_employee_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareCenter_Head',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('First_Name', models.CharField(blank=True, max_length=128)),
                ('Last_Name', models.CharField(blank=True, max_length=128)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone_number', models.IntegerField(max_length=128)),
                ('Address', models.CharField(blank=True, max_length=300)),
                ('Carecenter_document', models.FileField(blank=True, null=True, upload_to='carecenter_head')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='carecenter',
            name='CareCenter_Head',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='carecenter.carecenter_head'),
            preserve_default=False,
        ),
    ]