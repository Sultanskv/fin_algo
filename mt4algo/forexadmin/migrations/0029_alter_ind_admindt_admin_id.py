# Generated by Django 5.0.4 on 2024-10-21 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forexadmin', '0028_alter_ind_admindt_admin_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ind_admindt',
            name='admin_id',
            field=models.CharField(blank=True, default='574e1691', max_length=8, unique=True),
        ),
    ]
