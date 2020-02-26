from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly"]
API_SERVICE_NAME  = "youtubeAnalytics"
API_VERSION = "v2"

def authenticate():
    """Authentication handler for 
    authenticate with the API using OAUTH 2.0
    """
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def collector():
    # Authenticate using OAUTH 2.0
    creds = authenticate()

    # Instantiate api client
    Service = build(API_SERVICE_NAME , API_VERSION, credentials=creds)

    # Execute query in this case gather the shown metrics grouped by day from start to end
    results = Service.reports().query(
        ids='channel==MINE',
        startDate='2017-01-01',
        endDate='2017-12-31',
        metrics='estimatedMinutesWatched,views,likes,subscribersGained',
        dimensions='day',
        sort='day'
        ).execute()

    return results


if __name__ == '__main__':
    print(collector())