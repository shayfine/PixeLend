# Generated by Django 4.2 on 2023-04-23 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_rename_product_ex_product_extended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='max_time',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_amount',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_time',
            field=models.PositiveIntegerField(null=True),
        ),
    ]