# Generated by Django 4.2.19 on 2025-02-12 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('total_distance', models.FloatField()),
                ('estimated_duration', models.FloatField()),
                ('preferred_fuel_type', models.CharField(max_length=50)),
                ('cargo_capacity', models.FloatField()),
                ('route_status', models.CharField(choices=[('active', 'Active'), ('seasonal', 'Seasonal'), ('under_construction', 'Under Construction')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'routes',
            },
        ),
        migrations.CreateModel(
            name='RouteLanes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lane', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_lanes', to='ports.lane')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_lanes', to='routes.route')),
            ],
            options={
                'db_table': 'routes_lanes_rel',
            },
        ),
        migrations.AddField(
            model_name='route',
            name='lanes',
            field=models.ManyToManyField(related_name='routes', through='routes.RouteLanes', to='ports.lane'),
        ),
    ]
