import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv, find_dotenv, set_key
import json
import base64

if not os.getenv('VERCEL_ENV'):
    dotenv_path = find_dotenv()
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        raise FileNotFoundError("The .env file was not found.")


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
    creds = None

    if token := os.getenv("TOKEN_PICKLE_BASE64"):
        creds = pickle.loads(base64.b64decode(token))

    if not creds or not creds.valid:
        print("Authenticating...")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(json.loads(os.getenv("GOOGLE_CREDENTIALS")), SCOPES)
            creds = flow.run_local_server(port=0)

        set_key(dotenv_path, "TOKEN_PICKLE_BASE64", base64.b64encode(pickle.dumps(creds)).decode("utf-8"))
    print("Authenticated successfully!")
    return creds