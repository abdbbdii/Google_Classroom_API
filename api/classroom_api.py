import requests
from datetime import datetime, timezone
from .appSettings import appSettings


def get_course_announcements(service, course_id):
    """
    Fetches announcements for a given course.
    """
    try:
        announcements = service.courses().announcements().list(courseId=course_id).execute()
        return announcements.get("announcements", [])
    except Exception as e:
        print(f"An error occurred while fetching announcements for course {course_id}: {e}")
        return []


def get_coursework(service, course_id):
    """
    Fetches coursework for a given course.
    """
    try:
        coursework = service.courses().courseWork().list(courseId=course_id).execute()
        return coursework.get("courseWork", [])
    except Exception as e:
        print(f"An error occurred while fetching coursework for course {course_id}: {e}")
        return []


def get_materials(service, course_id):
    """
    Fetches materials for a given course.
    """
    try:
        materials = service.courses().courseWorkMaterials().list(courseId=course_id).execute()
        return materials.get("courseWorkMaterial", [])
    except Exception as e:
        print(f"An error occurred while fetching materials for course {course_id}: {e}")
        return []


def send_request(item, service):
    """
    Sends a request to a specified webhook URL.
    """
    try:
        profile = service.userProfiles().get(userId=item["course"]["ownerId"]).execute()
        owner_name = profile.get("name", {}).get("fullName")
    except Exception as e:
        owner_name = None
    item["course"]["ownerName"] = owner_name
    response = requests.post(
        appSettings.webhook_url,
        headers={"Content-Type": "application/json"},
        json=item,
    )
    print("Response:", response.status_code, response.text)


def parse_datetime(dt_str):
    """
    Parses a datetime string that may or may not include fractional seconds.
    """
    try:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def notify_new_activity(service):
    """
    Checks for new activities (announcements, coursework, materials) in the courses and notifies through a webhook.
    """

    last_check = appSettings.last_check = datetime.fromisoformat(appSettings.last_check).replace(tzinfo=timezone.utc) if appSettings.last_check is not None else datetime.now(timezone.utc)
    current_time = datetime.now(timezone.utc)
    appSettings.update("last_check", current_time.isoformat())

    try:
        courses = service.courses().list().execute().get("courses", [])
        for course in courses:
            print(f"Checking for new activity in course {course['name']}...")
            announcements = get_course_announcements(service, course["id"])
            for announcement in announcements:
                announcement_time = parse_datetime(announcement["updateTime"])
                if announcement_time > last_check:
                    print("New announcement found:", announcement)
                    send_request({"content": {"course": course, "activity": announcement, "type": "announcement"}}, service)

            coursework = get_coursework(service, course["id"])
            for work in coursework:
                work_time = parse_datetime(work["updateTime"])
                if work_time > last_check:
                    print("New coursework found:", work)
                    send_request({"content": {"course": course, "activity": work, "type": "coursework"}}, service)

            materials = get_materials(service, course["id"])
            for material in materials:
                material_time = parse_datetime(material["updateTime"])
                if material_time > last_check:
                    print("New material found:", material)
                    send_request({"content": {"course": course, "activity": material, "type": "material"}}, service)

    except Exception as e:
        print(f"An error occurred while checking for new activity: {e}")
