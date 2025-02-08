# Generated by Django 5.0.4 on 2024-10-01 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ind_adminDT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_id', models.CharField(blank=True, default='88c8273e', max_length=8, unique=True)),
                ('admin_name_first', models.CharField(blank=True, max_length=50, null=True)),
                ('admin_name_last', models.CharField(blank=True, max_length=50, null=True)),
                ('admin_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('admin_password', models.CharField(blank=True, max_length=50, null=True)),
                ('admin_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('admin_verify_code', models.CharField(blank=True, max_length=15, null=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrderAngelOne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clint', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=50)),
                ('tradingsymbol', models.CharField(max_length=50)),
                ('symboltoken', models.CharField(max_length=50)),
                ('transaction_type', models.CharField(max_length=20)),
                ('order_type', models.CharField(max_length=20)),
                ('quantity', models.IntegerField()),
                ('segment_type', models.CharField(max_length=20)),
                ('squareoff', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stoploss', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_id', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
