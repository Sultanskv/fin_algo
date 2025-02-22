# Generated by Django 5.0.6 on 2024-12-28 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_alter_clientdetail_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientdetail',
            name='telegram_chat_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='clientdetail',
            name='selected_option',
            field=models.CharField(choices=[('A', 'Route'), ('B', 'Detour'), ('C', 'Destination'), ('D', 'Demograph'), ('M', 'Messanger')], default='M', max_length=1),
        ),
        migrations.AlterField(
            model_name='clientdetail',
            name='user_id',
            field=models.CharField(default='2753fd35', max_length=8, unique=True),
        ),
    ]
