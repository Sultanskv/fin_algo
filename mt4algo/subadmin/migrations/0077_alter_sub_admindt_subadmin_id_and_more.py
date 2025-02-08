# Generated by Django 5.0.6 on 2025-01-30 12:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subadmin', '0076_alter_sub_admindt_subadmin_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_admindt',
            name='subadmin_id',
            field=models.CharField(blank=True, default='09f8935d', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='sub_admindt',
            name='subadmin_last_login',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 31, 12, 10, 10, 409095, tzinfo=datetime.timezone.utc), verbose_name='last login'),
        ),
    ]
