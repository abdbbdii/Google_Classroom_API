# Django Classroom Activity Notifier

## Overview

This Django project checks for new activities (announcements, coursework, and materials) in Google Classroom courses and sends notifications to a specified webhook URL. The project integrates with the Google Classroom API and is designed to run periodic checks for updates, ensuring that new activities are promptly notified.

## Features

- **Fetch Announcements:** Retrieves the latest announcements for a course.
- **Fetch Coursework:** Retrieves the latest coursework for a course.
- **Fetch Materials:** Retrieves the latest course materials for a course.
- **Send Webhook Notifications:** Sends new activities to a specified webhook URL.
- **Activity Monitoring:** Checks for new activities based on the last check timestamp and triggers notifications.

## Setup

1. **Google Classroom API Setup:**
   - Enable the Google Classroom API for your project on the Google Cloud Console.
   - Obtain the necessary OAuth 2.0 credentials and store them securely.

2. **Django Configuration:**
   - Clone this repository.
   - Install the required dependencies by running `pip install -r requirements.txt`.
   - Set up your `appSettings` with the following:
     - `webhook_url`: The URL where notifications will be sent.
     - `last_check`: The timestamp of the last check (optional, will be updated automatically).

3. **Service Authentication:**
   - Implement the `authenticate()` function to handle OAuth 2.0 authentication and obtain the credentials necessary to access the Google Classroom API.

4. **Run the Project:**
   - Start the Django server using `python manage.py runserver`.
   - Access the endpoint that triggers `notify_new_activity` to start checking for updates.

## Usage

- **Trigger Activity Check:**
  - Make a GET request to the endpoint where `notify_new_activity` is called. This will initiate the process of checking for new announcements, coursework, and materials, and send notifications if new activities are found.

- **Customizing Notifications:**
  - Modify the `send_request(item)` function to customize how notifications are sent to the webhook.

## Code Explanation

- **`get_course_announcements(service, course_id)`**: Fetches announcements for a specific course.
- **`get_coursework(service, course_id)`**: Fetches coursework for a specific course.
- **`get_materials(service, course_id)`**: Fetches materials for a specific course.
- **`send_request(item)`**: Sends a notification to the configured webhook URL.
- **`parse_datetime(dt_str)`**: Parses a datetime string from the Google Classroom API.
- **`notify_new_activity(service)`**: Checks for new activities in all courses and sends notifications if new activities are found.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
