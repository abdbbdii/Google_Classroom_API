from django.db import models

class Settings(models.Model):
    webhook_url = models.TextField(default="", null=True)
    webhook_url_test = models.TextField(default="", null=True)
    google_creds = models.TextField(default="", null=True)
    last_check = models.TextField(default="", null=True)
    utils_server_url = models.TextField(default="", null=True)
    utils_server_password = models.TextField(default="", null=True)
