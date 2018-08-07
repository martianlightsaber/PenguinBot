from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from extractnumbers import extract_numbers

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Display Chart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getBorderPrediction(region):
    discordOutput = 'Border Prediction\n'
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

    if region = "EN":
        spreadsheetId = '1Qaxod58OwaEg0xWG-rqt6VCGtUawI0ghzgR04X6WplY'      
        sheetName = 'Rapper Cecil Event Chart'
        rangeName = sheetName+'!H3:I10'

        ###retreive range from spreadsheet
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName, majorDimension='ROWS').execute()
        values = result.get('values', [])

        ###set values into string
        for row in values:
            discordOutput = discordOutput+'{:<5}{:<8}\n'.format(row[0], row[1])

    if region = "JP":
        spreadsheetId = '1Qaxod58OwaEg0xWG-rqt6VCGtUawI0ghzgR04X6WplY'    
        sheetName = 'Rapper Cecil Event Chart'
        rangeName = sheetName+'!H3:I10'

        ###retreive range from spreadsheet
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName, majorDimension='ROWS').execute()
        values = result.get('values', [])

        ###set values into string
        for row in values:
            discordOutput = discordOutput+'{:<5}{:<8}\n'.format(row[0], row[1])

    else:
        discordOutput = 'Please specify region (EN/JP)'

    return discordOutput

        


if __name__ == '__main__':
    main()
