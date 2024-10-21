#import datetime
from datetime import datetime, timezone
#from zoneinfo import ZoneInfo
from tzlocal import get_localzone

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.now(timezone.utc)
    rfc3339_timestamp = now.isoformat()

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=rfc3339_timestamp,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    #local_tz = ZoneInfo('America/Chicago')  # Change to your local timezone

    # Get the local time zone
    local_tz = get_localzone()

    for event in events:
        summary = event.get('summary', 'No summary available')
        date = event['start'].get('date')
        startTime = event['start'].get('dateTime')
        location = event.get('location', 'No location specified')

        if startTime:
            try:
                # Parse the startTime as a naive datetime and assume it's in UTC
                event_time_utc = datetime.fromisoformat(startTime)
                # Convert to local time
                local_time = event_time_utc.astimezone(local_tz)
                formattedTime = local_time.strftime("%I:%M %p")
                #formattedDate = local_time.strftime("%Y-%m-%d")
                formattedDate = local_time.strftime("%m %d, %Y")
            except ValueError as e:
                print(f"Error parsing time: {e}")
                formattedTime = "none"
                formattedDate = "none"
        else:
            print("Start time is not available.")
            formattedTime = "none"
            formattedDate = "none"

        # Print the event details
        print(f"{summary}\n{date}\nLocation: {location}\nTime: {formattedTime}\ndate : {formattedDate}\n")


  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()