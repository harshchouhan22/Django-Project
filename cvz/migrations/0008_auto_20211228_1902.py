# Generated by Django 3.1.7 on 2021-12-28 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carecenter', '0007_auto_20211228_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carecenter_employee',
            name='employee_image',
            field=models.ImageField(blank=True, null=True, upload_to='employee_pics'),
        ),
    ]
