# Generated by Django 5.0.6 on 2025-02-06 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0039_kyc_agreement_file_alter_clientdetail_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdetail',
            name='user_id',
            field=models.CharField(default='bafa1bd2', max_length=8, unique=True),
        ),
    ]
