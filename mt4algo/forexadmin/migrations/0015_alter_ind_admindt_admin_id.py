# Generated by Django 5.1.1 on 2024-10-18 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forexadmin', '0014_alter_ind_admindt_admin_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ind_admindt',
            name='admin_id',
            field=models.CharField(blank=True, default='c97d5ef9', max_length=8, unique=True),
        ),
    ]
