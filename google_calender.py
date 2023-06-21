import os
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth
import googleapiclient.discovery 


SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = None

def calender_API_get():
    global creds
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.isfile('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


def calender_event_get():
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow() .isoformat() + 'Z' # 'Z' indicates UTC time
        summary_fromtime = '2022-01-01T00:00:00Z'
        print('---Getting the upcoming 500 events、直近500の予定を取得します---')
        events_result = service.events().list(
            calendarId='16ed261fe7859dc00b3d1847ee712d8aa1775601a58bce9fb43a0b200320223b@group.calendar.google.com'
            , timeMin=summary_fromtime, maxResults=500, singleEvents=True, orderBy='startTime'
            ).execute()
        events = events_result.get('items', [])

        """
        #events_checkの戻り値をdeadlineとsummaryにした場合
        events_check = []
        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date')) #予定の全情報(items)が入っているeventsから、必要な情報をeventで回して抜き出す。
            summary = event['summary']
            #print(event)
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ') #文字列から日付へ
            start_time = start_time + datetime.timedelta(hours=9) #UTC→JST(標準時変更)
            #event = datetime.datetime.strptime(event, '%Y-%m-%dT%H:%M:%S:%Z')
            #start = datetime.datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
            #events_check.append(start[:-6])
            events_check.append((start_time, summary))
        print(events_check)
        """

        #events_checkの戻り値をsummaryにした場合
        events_check = []
        for event in events:
            summary_name = event['summary']
            events_check.append(summary_name)
            print(summary_name)

        if not events:
            print('No upcoming events found.')
        else:
            return events_check

        # Prints the start and name of the next 50 events
        """
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        """

    except HttpError as error:
        print('An error occurred: %s' % error)


def calender_event_insert(report_title,corse_name, deadline):
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': report_title + "/" + corse_name,
            'description': 'レポート期限',
            'start': {
            'dateTime': deadline,
            'timeZone': 'Japan',
            },
            'end': {
            'dateTime': deadline,
            'timeZone': 'Japan',
            },
            'colorId':3
        }
        event = service.events().insert(
            calendarId='16ed261fe7859dc00b3d1847ee712d8aa1775601a58bce9fb43a0b200320223b@group.calendar.google.com',
            body=event
            ).execute()

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    calender_API_get()
    calender_event_get()