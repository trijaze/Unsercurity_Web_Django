# Generated by Django 5.0.6 on 2025-04-09 12:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0002_borrowslip_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowslip',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='borrowslip',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
