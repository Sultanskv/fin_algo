# Generated by Django 5.0.6 on 2024-12-28 09:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subadmin', '0051_alter_sub_admindt_subadmin_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_admindt',
            name='subadmin_id',
            field=models.CharField(blank=True, default='304b351d', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='sub_admindt',
            name='subadmin_last_login',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 29, 9, 57, 47, 423429, tzinfo=datetime.timezone.utc), verbose_name='last login'),
        ),
    ]
