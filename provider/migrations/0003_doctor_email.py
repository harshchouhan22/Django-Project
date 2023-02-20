# Generated by Django 3.1.7 on 2021-12-24 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_auto_20211221_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='email',
            field=models.EmailField(default=2, max_length=254, unique=True, verbose_name='email address'),
            preserve_default=False,
        ),
    ]