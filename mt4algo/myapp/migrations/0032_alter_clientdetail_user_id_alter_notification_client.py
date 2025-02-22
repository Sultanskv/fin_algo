# Generated by Django 5.0.6 on 2024-12-28 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0031_alter_clientdetail_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdetail',
            name='user_id',
            field=models.CharField(default='ab9975a1', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='myapp.clientdetail'),
        ),
    ]
