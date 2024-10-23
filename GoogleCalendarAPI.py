# places next 15 events into lists of today or future

from datetime import datetime, timezone
from tzlocal import get_localzone

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

        try:
            service = build("calendar", "v3", credentials=self.creds)

            # Call the Calendar API
            self.now = datetime.now(timezone.utc)
            rfc3339_timestamp = self.now.isoformat()

            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=rfc3339_timestamp,
                    maxResults=15,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

        # Get the local time zone
            local_tz = get_localzone()

            for event in events:
                summary = event.get('summary', 'No summary available')
                #date = event['start'].get('date')#recurring events
                #eventDate = "No Date"
                #startTime = event['start'].get('dateTime')#one time events
                #eventTime = "No Time"
                location = event.get('location', 'No location specified')
                #print(f"{summary}\n")
                # if date:
                #     if date == now.date():
                #         self.todayEvents.append(event)
                #     else:
                #         self.futureEvents.append(event)
                if "dateTime" in event["start"]:#single event
                    #process horrible date formatting
                    #eventDate = self.processDate(event["start"]["dateTime"])
                    dateTimeString = self.processDateTime(summary, event["start"]["dateTime"], location)
                    
                
                elif "date" in event["start"]:#recurring events - format doesn't make you hate google even more
                    #process not so horrible formatting
                    #eventDate = self.processDate(event["start"]["date"])
                    #eventTime = "All Day"
                    dateString = self.processDate(summary, event["start"]["date"], location)


              
                # if startTime:
                #     try:
                #         # Parse the startTime as a naive datetime and assume it's in UTC
                #         event_time_utc = datetime.fromisoformat(startTime)
                #         # Convert to local time
                #         local_time = event_time_utc.astimezone(local_tz)
                #         formattedTime = local_time.strftime("%I:%M %p")
                #         formattedDate = local_time.strftime("%Y-%m-%d")
                #         if formattedDate == now.date():
                #             self.todayEvents.append(event)
                #         else:
                #             self.futureEvents.append(event)
                #     except ValueError as e:
                #         print(f"Error parsing time: {e}")
                #         formattedTime = "none"
                #         formattedDate = "none"
                # else:
                #     formattedTime = "none"
                #     formattedDate = "none"

          

        except HttpError as error:
            print(f"An error occurred: {error}")

    def processDateTime(self, summary, dateTime, location):
        print(f"Summary: {summary}")
        print(f"DateTime: {dateTime}")
        print(f"location: {location}")

    def processDate(self, summary, date, location):
        print(f"Summary: {summary}")
        print(f"Date is : {date}")
        print("Time: All Day")
        print(f"Location: {location}")
        # if date == self.now.date():
        #     print("event is today")
        # else:
        #     print("event is not today")




# calender = GoogleCalenderAPI()
# print(calender.todayEvents)
# print(calender.futureEvents)