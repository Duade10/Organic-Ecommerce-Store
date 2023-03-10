# Generated by Django 3.2 on 2022-12-01 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('description', models.TextField(blank=True, null=True)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=9)),
                ('in_stock', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/product/')),
                ('category', models.ManyToManyField(related_name='products', to='categories.Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('file', models.ImageField(upload_to='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='products.product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
    ]
