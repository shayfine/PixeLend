# Generated by Django 4.2 on 2023-05-16 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_rented_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='rented',
            name='question',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
