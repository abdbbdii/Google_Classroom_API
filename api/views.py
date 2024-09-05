import pickle
import base64

from django.http import JsonResponse
from .classroom_api import notify_new_activity
from googleapiclient.discovery import build

import requests
from .appSettings import appSettings
import json


def get(request):
    r = requests.get(
        appSettings.utils_server_url + "service/google_auth/",
        json={
            "password": appSettings.utils_server_password,
            "token_pickle_base64": appSettings.token_pickle_base64,
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
        
    if r.json().get("token_pickle_base64") != appSettings.token_pickle_base64:
        appSettings.update("token_pickle_base64", json.loads(r.json().get("token_pickle_base64")))

    service = build("classroom", "v1", credentials=pickle.loads(base64.b64decode(appSettings.token_pickle_base64)))
    notify_new_activity(service)

    return JsonResponse({"message": "Notification sent successfully."})
