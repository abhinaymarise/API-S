import os.path,json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
credentials_path="C:/Users/Abhinay/Documents/API/Question_19/credentials.json"
token_path="C:/Users/Abhinay/Documents/API/Question_19/token.json"


def get_service():

    cred=None

    if os.path.exists(token_path):
        cred = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            cred = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(cred.to_json())

    service = build('gmail', 'v1', credentials=cred)
    return service