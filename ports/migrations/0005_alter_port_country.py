# Generated by Django 4.2.19 on 2025-02-11 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ports', '0004_alter_port_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='port',
            name='country',
            field=models.CharField(max_length=100),
        ),
    ]
