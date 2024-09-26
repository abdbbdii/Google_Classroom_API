import pickle
import base64
import traceback

import requests
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from googleapiclient.discovery import build

from .appSettings import appSettings
from .classroom_api import notify_new_activity


def get(request):
    try:
        try:
            service = build("classroom", "v1", credentials=pickle.loads(base64.b64decode(appSettings.token_pickle_base64)))
            async_to_sync(notify_new_activity)(service)
        except Exception as e:
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

            print(r.json())

            if r.status_code != 200:
                return JsonResponse({"error": r.json().get("message")}, status=500)

            if r.json().get("token_pickle_base64") != appSettings.token_pickle_base64:
                appSettings.update("token_pickle_base64", r.json().get("token_pickle_base64"))

            return JsonResponse({"message": str(traceback.format_exc())})

        return JsonResponse({"message": "Notification sent successfully."})

    except Exception as e:
        return JsonResponse({"message": str(traceback.format_exc())}, status=500)
