# Generated by Django 2.2.4 on 2020-12-23 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rate_me', '0003_auto_20201223_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='admin',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='rate_me.user_roles'),
        ),
    ]