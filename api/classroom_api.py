import requests
from datetime import datetime, timezone
from .appSettings import appSettings


def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def get_new_item(service, course, item_type, last_check):
    if item_type == "announcements":
        items = service.courses().announcements().list(courseId=course["id"], orderBy="updateTime desc").execute()
    elif item_type == "courseWork":
        items = service.courses().courseWork().list(courseId=course["id"], orderBy="updateTime desc").execute()
    elif item_type == "courseWorkMaterial":
        items = service.courses().courseWorkMaterials().list(courseId=course["id"], orderBy="updateTime desc").execute()

    for item in items.get(item_type, []):
        if parse_datetime(item["updateTime"]) > last_check:
            print(f"New item found:")
            print(item)
            try:
                response = requests.post(
                    appSettings.webhook_url,
                    headers={"Content-Type": "application/json"},
                    json={"course": course, "activity": item, "type": item_type, "is_new": (parse_datetime(item["creationTime"]) - parse_datetime(item["updateTime"])).total_seconds() < 300},
                )
            except:
                response = requests.post(
                    appSettings.webhook_url,
                    headers={"Content-Type": "application/json"},
                    json={"course": course, "activity": item, "type": item_type, "new": True},
                )
            print("Response:", response.status_code, response.text)
        else:
            break


def notify_new_activity(service):
    print("Last check:", appSettings.last_check)
    last_check = datetime.fromisoformat(appSettings.last_check).replace(tzinfo=timezone.utc) if appSettings.last_check is not None else datetime.now(timezone.utc)
    appSettings.update("last_check", datetime.now(timezone.utc).isoformat())

    courses = service.courses().list().execute().get("courses", [])
    for course in courses:
        print(f"Checking for new activity in course {course['name']}...")
        get_new_item(service, course, "announcements", last_check)
        get_new_item(service, course, "courseWork", last_check)
        get_new_item(service, course, "courseWorkMaterial", last_check)
