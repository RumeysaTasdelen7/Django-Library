# Generated by Django 5.0.2 on 2024-03-25 11:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("User", "0002_remove_user_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]