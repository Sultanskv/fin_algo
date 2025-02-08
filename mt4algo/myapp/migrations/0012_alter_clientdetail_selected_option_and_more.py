# Generated by Django 5.0.6 on 2024-12-09 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_clientdetail_user_id_clientmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdetail',
            name='selected_option',
            field=models.CharField(choices=[('A', 'Route'), ('B', 'Detour'), ('C', 'Destination'), ('D', 'Demograph'), ('M', 'Messanger')], default='M', max_length=1),
        ),
        migrations.AlterField(
            model_name='clientdetail',
            name='user_id',
            field=models.CharField(default='eb57d18c', max_length=8, unique=True),
        ),
    ]
