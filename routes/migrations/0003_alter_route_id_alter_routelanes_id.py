# Generated by Django 4.2.19 on 2025-02-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0002_auto_20250213_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='routelanes',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
