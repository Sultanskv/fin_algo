# Generated by Django 5.0.4 on 2024-10-21 11:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subadmin', '0032_alter_sub_admindt_subadmin_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_admindt',
            name='subadmin_id',
            field=models.CharField(blank=True, default='ba666ab0', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='sub_admindt',
            name='subadmin_last_login',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 22, 11, 17, 0, 623669, tzinfo=datetime.timezone.utc), verbose_name='last login'),
        ),
    ]
