# Generated by Django 5.0.2 on 2024-02-24 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone', models.CharField(db_index=True, max_length=30)),
                ('address', models.CharField(max_length=255)),
                ('email', models.EmailField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.CharField(max_length=12)),
                ('opening_hour', models.CharField(max_length=6)),
                ('closing_hour', models.CharField(max_length=6)),
            ],
        ),
    ]
