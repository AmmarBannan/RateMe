# Generated by Django 2.2.4 on 2020-12-27 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate_me', '0008_auto_20201227_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car_type',
            name='model',
        ),
    ]
