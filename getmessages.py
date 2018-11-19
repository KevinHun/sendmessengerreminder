from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET = '1nixeVDOCTsN_oRp3EQYqFoRyPKtBiYZBYhzwNt7Yf60'
RANGE = 'Data!A2:D'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET,
                                range=RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Subject, Amount, Done:')
        data = {"messages": []}

        for row in values:
            if not (len(row) == 4 or len(row) == 3):
                raise ValueError("Row does not have 3 or 4 values")

            # Check if row array length is lower then 4, if so column "Betaald" isn't filled in.
            if len(row) < 4:
                row.append("no")

            print('{}, {}, {}, {}'.format(row[0], row[1], row[2], row[3]))
            if not row[3] == "ja":
                message = {"receiver": row[0], "text": "Hallo, je moet me nog {} euro voor volgende zaken: {}, kan je me die overschrijven? Thanks! Indien je het gedaan hebt, laat het me effe weten en dan laat ik je met rust :)".format(row[2], row[1])}
                data["messages"].append(message)

        print(data)
        with open('messages.json', 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()