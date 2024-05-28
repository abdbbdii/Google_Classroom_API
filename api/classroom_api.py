import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv, find_dotenv, set_key

dotenv_path = find_dotenv()
# if not dotenv_path:
#     raise FileNotFoundError("The .env file was not found.")
load_dotenv(dotenv_path)

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
    "https://www.googleapis.com/auth/classroom.announcements.readonly",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
]


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


def send_request(item):
    """
    Sends a request to a specified webhook URL.
    """
    response = requests.post(
        os.getenv("WEBHOOK_URL"),
        headers={"Content-Type": "application/json"},
        json=item,
    )
    print("Response:", response.status_code, response.text)


def notify_new_activity(service):
    """
    Checks for new activities (announcements, coursework, materials) in the courses and notifies through a webhook.
    """

    last_check = os.getenv("LAST_CHECK")
    last_check = datetime.fromisoformat(last_check).replace(tzinfo=timezone.utc) if last_check is not None else datetime.now(timezone.utc)
    current_time = datetime.now(timezone.utc)

    try:
        courses = service.courses().list().execute().get("courses", [])
        for course in courses:
            print(f"Checking for new activity in course {course['name']}...")
            announcements = get_course_announcements(service, course["id"])
            for announcement in announcements:
                announcement_time = datetime.strptime(announcement["updateTime"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                if announcement_time > last_check:
                    print("New announcement found:", announcement)
                    send_request({"content": {"course": course, "activity": announcement, "type": "announcement"}})

            coursework = get_coursework(service, course["id"])
            for work in coursework:
                work_time = datetime.strptime(work["updateTime"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                if work_time > last_check:
                    print("New coursework found:", work)
                    send_request({"content": {"course": course, "activity": work, "type": "coursework"}})

            materials = get_materials(service, course["id"])
            for material in materials:
                material_time = datetime.strptime(material["updateTime"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                if material_time > last_check:
                    print("New material found:", material)
                    send_request({"content": {"course": course, "activity": material, "type": "material"}})

    except Exception as e:
        print(f"An error occurred while checking for new activity: {e}")

    set_key(dotenv_path, "LAST_CHECK", current_time.isoformat())