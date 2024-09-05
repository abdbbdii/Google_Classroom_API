from django.http import JsonResponse
from .classroom_api import notify_new_activity
from googleapiclient.discovery import build

import requests
from .appSettings import appSettings
import json


def get(request):
    r = requests.get(
        appSettings.utils_server + "service/google_auth/",
        json={
            "password": appSettings.utils_server_password,
            "scopes": [
                "https://www.googleapis.com/auth/classroom.courses.readonly",
                "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
                "https://www.googleapis.com/auth/classroom.announcements.readonly",
                "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
            ],
        },
    )
    if r.status_code != 200:
        return JsonResponse({"error": "Failed to authenticate with Google."}, status=500)
    appSettings.update("google_creds", json.loads(r.json().get("google_creds")))

    service = build("classroom", "v1", credentials=appSettings.google_creds)
    notify_new_activity(service)

    return JsonResponse({"message": "Notification sent successfully."})
