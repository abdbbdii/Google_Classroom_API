import json
import pickle

import base64
import google.auth.exceptions
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

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

    print("Checking stored credentials...")
    creds = None

    # Retrieve stored token if available
    if token := appSettings.token_pickle_base64:
        try:
            creds = pickle.loads(base64.b64decode(token))
        except Exception as e:
            print(f"Failed to load credentials: {e}")
            creds = None

    # Check if the credentials are valid and refresh if needed
    if creds and creds.valid:
        print("Using stored credentials.")
    elif creds and creds.expired and creds.refresh_token:
        try:
            print("Refreshing access token...")
            creds.refresh(Request())
            appSettings.update("token_pickle_base64", base64.b64encode(pickle.dumps(creds)).decode("utf-8"))
            print("Token refreshed successfully.")
        except google.auth.exceptions.RefreshError:
            print("Token refresh failed. Starting new authentication flow...")
            creds = None

    # If no valid credentials, authenticate via Google
    if not creds or not creds.valid:
        print("Authenticating with Google...")
        flow = InstalledAppFlow.from_client_config(json.loads(appSettings.google_credentials), SCOPES)
        creds = flow.run_local_server(port=0)
        appSettings.update("token_pickle_base64", base64.b64encode(pickle.dumps(creds)).decode("utf-8"))
        print("Authenticated and token stored successfully.")

    return creds
