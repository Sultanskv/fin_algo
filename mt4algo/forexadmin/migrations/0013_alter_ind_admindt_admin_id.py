# Generated by Django 5.0.4 on 2024-10-10 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forexadmin', '0012_alter_ind_admindt_admin_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ind_admindt',
            name='admin_id',
            field=models.CharField(blank=True, default='9676fdf6', max_length=8, unique=True),
        ),
    ]
