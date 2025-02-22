# Generated by Django 5.0.6 on 2025-02-06 06:29

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subadmin', '0077_alter_sub_admindt_subadmin_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_admindt',
            name='sub_admin_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sub_admindt',
            name='subadmin_Term_condition',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sub_admindt',
            name='subadmin_account_type',
            field=models.CharField(choices=[('demo', 'Demo'), ('live', 'Live')], default='live', max_length=10),
        ),
        migrations.AddField(
            model_name='sub_admindt',
            name='subadmin_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sub_admindt',
            name='subadmin_ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sub_admindt',
            name='subadmin_paid_paln',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='sub_admindt',
            name='subadmin_id',
            field=models.CharField(blank=True, default='0ff7bcc6', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='sub_admindt',
            name='subadmin_last_login',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 7, 6, 29, 22, 382110, tzinfo=datetime.timezone.utc), verbose_name='last login'),
        ),
        migrations.CreateModel(
            name='SUBKYC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subadmin_national_id', models.FileField(blank=True, null=True, upload_to='subadmin_national_ids/')),
                ('subadmin_national_id_number', models.CharField(blank=True, max_length=20, null=True)),
                ('subadmin_national_id_name', models.CharField(blank=True, max_length=100, null=True)),
                ('subadmin_national_id_issue_date', models.DateField(blank=True, null=True)),
                ('subadmin_agreement_signed', models.BooleanField(default=False)),
                ('subadmin_agreement_file', models.FileField(blank=True, null=True, upload_to='subadmin_agreements/')),
                ('subadmin_terms_accepted', models.BooleanField(default=False)),
                ('subadmin_reference_text', models.TextField(blank=True, null=True)),
                ('subadmin_kyc_completed', models.BooleanField(default=False)),
                ('subadmin_video_file', models.FileField(blank=True, null=True, upload_to='subadmin_video_verifications/')),
                ('subadmin_video_verification_done', models.BooleanField(default=False)),
                ('reference_text', models.TextField(blank=True, null=True)),
                ('subadmin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kyc_details', to='subadmin.sub_admindt')),
            ],
        ),
    ]
