# Generated by Django 4.2.7 on 2025-06-17 12:38

from django.db import migrations, models
import django.db.models.deletion
import django_tenants.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('name', models.CharField(help_text='Company/Store name', max_length=100)),
                ('email', models.EmailField(help_text='Primary contact email', max_length=254)),
                ('description', models.TextField(blank=True, help_text='About the store')),
                ('is_active', models.BooleanField(default=True, help_text='Is store active?')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('on_trial', models.BooleanField(default=True)),
                ('paid_until', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tenants',
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('ssl_enabled', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='customers.tenant')),
            ],
            options={
                'db_table': 'domains',
            },
        ),
    ]
