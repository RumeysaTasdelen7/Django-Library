# Generated by Django 5.0.2 on 2024-03-21 15:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Book", "0002_alter_category_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="books",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="publisher",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
