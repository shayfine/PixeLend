# Generated by Django 4.2 on 2023-05-15 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_rented_explanation'),
    ]

    operations = [
        migrations.AddField(
            model_name='rented',
            name='answer',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
