# Generated by Django 3.2 on 2022-12-17 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold_in',
            field=models.CharField(max_length=10, null=True),
        ),
    ]