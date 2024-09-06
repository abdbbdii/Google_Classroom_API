import requests
from datetime import datetime, timezone
from .appSettings import appSettings


def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def get_new_item(service, course, item_type):
    items = service.courses().courseWorkMaterials().list(courseId=course["id"]).execute()
    for item in items.get(item_type, []):
        item_time = parse_datetime(item["updateTime"])
        if item_time > appSettings.last_check:
            print(f"New {item} found")
            # profile = service.userProfiles().get(userId=item["ownerId"]).execute()
            # owner_name = profile.get("name", {}).get("fullName")
            # item["ownerName"] = owner_name
            response = requests.post(
                appSettings.webhook_url,
                headers={"Content-Type": "application/json"},
                json={"course": course, "activity": item, "type": item_type},
            )
            print("Response:", response.status_code, response.text)


def notify_new_activity(service):
    appSettings.last_check = datetime.fromisoformat(appSettings.last_check).replace(tzinfo=timezone.utc) if appSettings.last_check is not None else datetime.now(timezone.utc)
    appSettings.update("last_check", datetime.now(timezone.utc).isoformat())

    courses = service.courses().list().execute().get("courses", [])
    for course in courses:
        print(f"Checking for new activity in course {course['name']}...")
        get_new_item(service, course, "announcements")
        get_new_item(service, course, "courseWork")
        get_new_item(service, course, "courseWorkMaterial")
