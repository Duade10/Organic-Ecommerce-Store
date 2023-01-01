# Generated by Django 3.2 on 2022-12-13 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20221213_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('paypal', 'PayPal'), ('paystack', 'PayStack')], max_length=8, null=True),
        ),
    ]
