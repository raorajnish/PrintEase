# Generated by Django 5.1.6 on 2025-03-04 08:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=255)),
                ('owner_name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('details_filled', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
