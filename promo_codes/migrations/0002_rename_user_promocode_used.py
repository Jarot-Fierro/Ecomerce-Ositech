# Generated by Django 4.2.13 on 2024-08-18 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promo_codes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promocode',
            old_name='user',
            new_name='used',
        ),
    ]
