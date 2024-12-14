from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.header import Header
import base64
import pickle
import os.path
from google.auth.transport.requests import Request

'''
python script for using the Gmail API for sending emails
to users when ther target price his lower then the current price
'''



SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE = './client_secret.json'
TOKEN_FILE = 'token.pickle'

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, _charset='utf-8')
    message['to'] = to
    message['from'] = sender
    message['subject'] = Header(subject, 'utf-8')
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')

def load_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def email_controller(recive_email , email_data):
    creds = load_credentials()
    service = build('gmail', 'v1', credentials=creds)
    
    email_body = email_data
    message = create_message("wineprocetracking@gmail.com", recive_email, "wine price tracking alert", email_body)
    send_message(service, "me", message)

