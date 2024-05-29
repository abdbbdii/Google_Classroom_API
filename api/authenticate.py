import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import base64
from .appSettings import appSettings

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
    "https://www.googleapis.com/auth/classroom.announcements.readonly",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
]


def authenticate():
    """
    Authenticates the user using OAuth2 credentials and returns the credentials object.
    """
    if not appSettings.google_credentials:
        raise ValueError("Google credentials not found in the database.")
    print("Authenticating...")
    creds = None

    if token := appSettings.token_pickle_base64:
        creds = pickle.loads(base64.b64decode(token))

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(json.loads(appSettings.google_credentials), SCOPES)
            creds = flow.run_local_server(port=0)

        appSettings.update("token_pickle_base64", base64.b64encode(pickle.dumps(creds)).decode("utf-8"))

    print("Authenticated successfully!")
    return creds
