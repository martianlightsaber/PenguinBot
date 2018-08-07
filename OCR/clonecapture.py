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
APPLICATION_NAME = 'Tier Recorder'


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

def find_last_row(values):
    if not values:
        print('No data found.')
    else:
        #print('Latest Cutoffs:')
        lastRow = len(values)
        for i, row in reversed(list(enumerate(values))):
            # Print columns A and E, which correspond to indices 0 and 4.
            if row[1] != '':
                #print(i, row[0])
                lastRow = i
                break
            #print('%s, %s' % (row[0], row[4]))
        latestRow = values[lastRow]
        #print('1%%: %s\n2%%: %s\n3%%: %s\n4%%: %s\n5%%: %s' % (latestRow[1], latestRow[2], latestRow[3], latestRow[4], latestRow[5]))
    return lastRow

def writeToSheets(ocr_output_raw,timestamp):
    didItWork = 'OCR failed, please try again or enter values manually'
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #spreadsheetId = '1AStF6YdzwtCFNYS8tbOMRJCuRcKVAgufS102Fbfm1FE'
    spreadsheetId = '14Av4hAYSEUBATzUPqVu4pa4Bg9kCw1AVxBAOZj0TLFY'

    sheetName = 'Romantic Tokiya Bot'
    columnStart = 'C'
    columnEnd = 'N'
    rowStart = '3'
    rowEnd = '171'
    editColumnStart = 'D'
    editColumnEnd = 'L'
    rangeName = sheetName+'!'+columnStart+rowStart+':'+columnEnd+rowEnd

    ###retreive range from spreadsheet
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName, majorDimension='ROWS').execute()
    values = result.get('values', [])

    ###find last filled row
    lastRow = find_last_row(values)

    ###read .txt file into an array
    scoreList, errorMessage = extract_numbers(ocr_output_raw)
    
    ###write array into row that matches time
    ###find row with recorded time
    recordedTime = timestamp[0:2]+':'+timestamp[2:4]
    print(recordedTime)
    for row in range(lastRow,len(values),1):
        if recordedTime == values[row][11]:
            print(values[row][0])
            if values[row][1] != '':
                didItWork = 'Error, row in gsheets not empty'
                break

            amendedScoreList = []
            scoreListCounter = 7
            ###RETHINK HOW TO DO THIS
            for column in range(8,0,-1):
                print(scoreList[scoreListCounter]+', '+values[lastRow][column])
                #while int(scoreList[scoreListCounter]) < int(values[lastRow][column]):
                #    scoreListCounter = scoreListCounter - 1
                if int(scoreList[scoreListCounter]) > int(values[lastRow][column]):
                    if int(scoreList[scoreListCounter]) - int(values[lastRow][column]) > 10000:
                        amendedScoreList.append(values[lastRow][column])
                    else:
                        amendedScoreList.append(scoreList[scoreListCounter])
                    scoreListCounter = scoreListCounter - 1
                else:
                    amendedScoreList.append(values[lastRow][column])
            amendedScoreList.reverse()
            amendedScoreList.append(scoreList[8])
            print(amendedScoreList)
            
            editedRow = str(int(rowStart)+row)
            editRange = sheetName+'!'+editColumnStart+editedRow+':'+editColumnEnd+editedRow
            write_score = {
                "range": editRange,
                "majorDimension": 'ROWS',
                "values": [amendedScoreList],
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheetId, range=editRange,
                valueInputOption='USER_ENTERED', body=write_score).execute()
            didItWork = 'OCR success! Please check the graph for anomalies.'
            break

    return didItWork

#if __name__ == '__main__':
#    main()
