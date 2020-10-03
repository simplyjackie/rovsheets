import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Google Sheet IDs
NC_MASTER_ID = '1T1HXFVGtfWgaXv5h66Rc77tdKeMOg_xSaEkq4PxuzbQ'
MENTOR_MASTER_ID = '13vdI0b4bN6uoYQIq5VBwLZUKtPVLEGnN77z3PDkrfIg'
INTERN_MASTER_ID = '14pEto7OK6BEDZ5UrhrrniSDI_4ec6a0UpcZA0dJU1gY'
SAMPLE_RANGE = 'A1:AA1000'

def df_from_sheet(sheet_id, range_id):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId= sheet_id, range= range_id).execute()
    values = result.get('values', [])
    df = pd.DataFrame(values[1:], columns=values[0])
    return df


def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Build Sheet Dataframes
    df_ncmaster = df_from_sheet(NC_MASTER_ID, SAMPLE_RANGE)
    df_mentorlist = df_from_sheet(MENTOR_MASTER_ID, 'A1:B70')
    df_internlist = df_from_sheet(INTERN_MASTER_ID, 'A1:B136')

    print(df_ncmaster)
    print(df_mentorlist)
    print(df_internlist)
    
    df_intern_not_password = df_internlist[df_internlist.email.isin(df_ncmaster.email)]
    print(df_intern_not_password)
 

main()

