from django.http import JsonResponse
from api.authenticate import authenticate
from api.classroom_api import notify_new_activity
from googleapiclient.discovery import build

service = build("classroom", "v1", credentials=authenticate())

def get(request):
    if request.method == "GET":
        try:
            notify_new_activity(service)
            return JsonResponse({"message": "Notification sent successfully."})
        except Exception as e:
            return JsonResponse({"message": f"An error occurred\n\n{e}"}, status=500)
