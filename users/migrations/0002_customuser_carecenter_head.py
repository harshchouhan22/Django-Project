# Generated by Django 3.1.7 on 2021-12-21 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='CareCenter_Head',
            field=models.BooleanField(default=False),
        ),
    ]