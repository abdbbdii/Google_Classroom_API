import os
from django.db import models
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) if not os.getenv("VERCEL_ENV") else None


class Settings(models.Model):
    webhook_url = models.TextField(default="", null=True)
    webhook_url_test = models.TextField(default="", null=True)
    google_credentials = models.TextField(default="", null=True)
    token_pickle_base64 = models.TextField(default="", null=True)
    last_check = models.TextField(default="", null=True)
