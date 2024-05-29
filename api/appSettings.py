import os
from .models import Settings
from dotenv import load_dotenv, find_dotenv
from django.conf import settings as django_settings

load_dotenv(find_dotenv()) if not os.getenv("VERCEL_ENV") else None


class AppSettings:
    def __init__(self) -> None:
        settings_values = {}

        try:
            settings = Settings.objects.first()
        except Exception as e:
            print(e)
            settings = None

        if not settings:
            settings = Settings()

        for field in Settings._meta.fields:
            value = getattr(settings, field.name)
            if not value or value == "":
                value = os.getenv(field.name.upper())
                if value:
                    setattr(settings, field.name, value)
            settings_values[field.name] = value

        settings.save()

        self.webhook_url = settings.webhook_url_test if django_settings.DEBUG else settings.webhook_url
        self.google_credentials = settings.google_credentials
        self.token_pickle_base64 = settings.token_pickle_base64
        self.last_check = settings.last_check

    def __str__(self) -> str:
        return f"""webhook_url: {self.webhook_url}
google_credentials: {self.google_credentials}
token_pickle_base64: {self.token_pickle_base64}
last_check: {self.last_check}"""

    def update(self, key, value):
        setattr(self, key, value)
        settings = Settings.objects.first()
        setattr(settings, key, value)
        settings.save()

    def empty(self):
        for field in self.__dict__:
            setattr(self, field, "")
        settings = Settings.objects.first()
        for field in settings._meta.fields:
            if field.name != "id":
                setattr(settings, field.name, "")
        settings.save()


# class AppSettings:
#     def __init__(self) -> None:
#         self.webhook_url = ""
#         self.google_credentials = ""
#         self.token_pickle_base64 = ""
#         self.last_check = ""

appSettings = AppSettings()