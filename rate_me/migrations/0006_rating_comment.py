# Generated by Django 2.2.4 on 2020-12-24 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate_me', '0005_auto_20201223_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='comment',
            field=models.TextField(max_length=255, null=True),
        ),
    ]