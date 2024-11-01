import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from gdoctableapppy import gdoctableapp

SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

DOCUMENT_ID = ""

def main():
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  resource = {
      "oauth2": creds,
      "documentId": "",
      "tableIndex": 0,
  }

  values = gdoctableapp.GetValues(resource)['values']

  result = []
  for i in range(1, len(values)):
    row = values[i]
    x = int(row[0])
    symbol = row[1]
    y = int(row[2])

    while y > len(result) -1:
      result.append("")

    string = result[y]
    string = string[:x] + symbol
    result[y] = string

  length = len(result)
  for i in range(length):
    print(result[length - i - 1])

if __name__ == "__main__":
  main()