# Generated by Django 3.2 on 2022-12-14 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_payment_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=200),
        ),
    ]
