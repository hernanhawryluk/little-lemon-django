# Generated by Django 5.0.2 on 2024-02-26 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_booking_created_booking_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='time',
            field=models.TimeField(),
        ),
    ]
