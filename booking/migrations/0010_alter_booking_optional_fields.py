# Generated by Django 4.2.19 on 2025-03-01 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_optionalfields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='optional_fields',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.optionalfields'),
        ),
    ]
