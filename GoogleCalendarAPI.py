# places next 15 events into lists of today or future

from datetime import datetime, timezone
from tzlocal import get_localzone
#import pytz

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalenderAPI:
    def __init__(self):
        self.todayEvents = []
        self.futureEvents = []
        self.localTimezone = get_localzone()
        self.todaysDate = datetime.now(self.localTimezone).date()
        self.scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                self.creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        self.requestCalendar()
    
    # retrieve calendar info
    def requestCalendar(self):
        try:
            self.todayEvents = []
            self.futureEvents = []
            service = build("calendar", "v3", credentials=self.creds)

            # Call the Calendar API
            self.now = datetime.now(timezone.utc)
            rfc3339_timestamp = self.now.isoformat()

            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=rfc3339_timestamp,
                    maxResults=6,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

            for event in events:
                summary = event.get('summary', 'No summary available')
                location = event.get('location', 'No location specified')
                if "dateTime" in event["start"]:#single event
                    dateTimeString = self.processDateTime(summary, event["start"]["dateTime"], location)
                                
                elif "date" in event["start"]:#recurring events
                    dateString = self.processDate(summary, event["start"]["date"], location)

        except HttpError as error:
            print(f"An error occurred: {error}")

    def processDateTime(self, summary, dateTime, location):
        event_time_utc = datetime.fromisoformat(dateTime)
        local_time = event_time_utc.astimezone(self.localTimezone)
        formattedTime = local_time.strftime("%I:%M %p")
        formattedDate = local_time.strftime("%m-%d-%Y")
        checkDate = local_time.date()
        tempDict = {
            "summary" : summary,
            "date" : formattedDate,
            "time" : formattedTime,
            "location" : location
        }
        
        if checkDate == self.todaysDate:
            self.todayEvents.append(tempDict)
        else:
            self.futureEvents.append(tempDict)

    def processDate(self, summary, date, location):
        checkDate = datetime.strptime(date, "%Y-%m-%d").date()
        tempDict = {
            "summary" : summary,
            "date" : date,
            "time" : "All Day",
            "location" : location
        }

        if checkDate == self.todaysDate:
            self.todayEvents.append(tempDict)
        else:
            self.futureEvents.append(tempDict)