# Generated by Django 5.0.2 on 2024-03-26 11:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("User", "0005_alter_user_managers_user_date_joined_user_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="createDate",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
