import logging
import pickle
import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def _parse_google_table(spreadsheetId, spreadsheetRange):
    logging.info('[reader] Parsing spreadsheet {}'.format(spreadsheetId))
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                ['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=spreadsheetId,
        range=spreadsheetRange
    ).execute()

    values = result.get('values', [])
    validated_values = []
    canonical_length = max([len(row) for row in values])

    for row in values:
        if len(row) != canonical_length:
            continue
        if None in row:
            continue
        validated_values.append(row)

    logging.info(
        '[reader] Finished parsing spreadsheet {}'.format(spreadsheetId)
    )
    return validated_values


def get_default_values_from_spreadsheet(spreadsheetId):
    values = _parse_google_table(spreadsheetId, 'A1:D1000000')
    dict_values = []
    for row in values:
        if len(row) < 4:
            continue
        dict_values.append({
            'to_addr': row[0],
            'html_text': row[1],
            'subject': row[2],
            'unsubscribe_link': row[3]
        })
    return dict_values
