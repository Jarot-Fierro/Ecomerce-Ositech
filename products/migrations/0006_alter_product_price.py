# Generated by Django 4.2.13 on 2024-08-09 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_brand_product_clothing_model_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0, max_length=8),
        ),
    ]