# Generated by Django 2.2.4 on 2020-12-23 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate_me', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_type',
            name='model',
            field=models.IntegerField(),
        ),
    ]
