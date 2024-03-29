# Generated by Django 5.0.2 on 2024-03-03 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.CharField(max_length=17, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=70)),
                ("builtIn", models.BooleanField(max_length=70)),
            ],
            options={
                "verbose_name_plural": "Yazarlar",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.CharField(max_length=17, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=80)),
                ("builtIn", models.BooleanField(default=False)),
                ("sequence", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name_plural": "Kategoriler",
            },
        ),
        migrations.CreateModel(
            name="Publisher",
            fields=[
                (
                    "id",
                    models.CharField(max_length=17, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=70)),
                ("builtIn", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "Yayınevleri",
            },
        ),
        migrations.CreateModel(
            name="Books",
            fields=[
                (
                    "id",
                    models.CharField(max_length=17, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=80)),
                ("isbn", models.CharField(max_length=17)),
                ("pageCount", models.IntegerField(blank=True, null=True)),
                ("sort", models.CharField(default="name", max_length=20)),
                ("publishDate", models.IntegerField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="images/"),
                ),
                ("loanable", models.BooleanField(default=True)),
                (
                    "shelfCode",
                    models.CharField(help_text="Format: WF-214", max_length=10),
                ),
                ("active", models.BooleanField(default=True)),
                ("featured", models.BooleanField(default=False)),
                ("createDate", models.DateTimeField(auto_now_add=True)),
                ("builtIn", models.BooleanField(default=False)),
                (
                    "authorId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Book.author"
                    ),
                ),
                (
                    "categoryId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Book.category"
                    ),
                ),
                (
                    "publisherId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Book.publisher"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Kitaplar",
            },
        ),
    ]
