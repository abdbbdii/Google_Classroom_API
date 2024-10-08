# Generated by Django 4.2.9 on 2024-05-29 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Classroom_API_Settings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("webhook_url", models.TextField(default="", null=True)),
                ("webhook_url_test", models.TextField(default="", null=True)),
                ("google_credentials", models.TextField(default="", null=True)),
                ("token_pickle_base64", models.TextField(default="", null=True)),
                ("last_check", models.TextField(default="", null=True)),
            ],
        ),
    ]
