# Generated by Django 4.2.9 on 2024-09-05 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_remove_settings_google_credentials_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="settings",
            old_name="google_creds",
            new_name="token_pickle_base64",
        ),
    ]