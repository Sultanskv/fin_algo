# Generated by Django 5.0.6 on 2024-12-28 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_alter_clientdetail_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdetail',
            name='user_id',
            field=models.CharField(default='07ae79b7', max_length=8, unique=True),
        ),
    ]
