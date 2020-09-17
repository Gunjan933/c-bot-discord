import gspread
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
import pandas as pd

class google_spreadsheet:

  def __init__(self):
    self.googleAPI = '../cainvas-scholar.json'
    self.scope = ['https://www.googleapis.com/auth/drive']
    self.credentials = service_account.Credentials.from_service_account_file(self.googleAPI)
    self.scopedCreds = self.credentials.with_scopes(self.scope)
    self.sheetName = "Cainvas Scholar Registration (Responses)"
    self.sheet =  self.get_sheet()
    self.df = pd.DataFrame(self.sheet.get_all_records())

  def get_sheet(self):
    while True:
      try:
        gc = gspread.Client(auth=self.scopedCreds)
        gc.session = AuthorizedSession(self.scopedCreds)
        sheet = gc.open(self.sheetName).sheet1
        return sheet
      except:
        print("Authentication error, trying again")
        pass

  def search_details(self, uniqueID):
    df = self.df.loc[(self.df['Discord Username'] == uniqueID) | (self.df['Email Address'] == uniqueID)]
    return None if df.empty else df


# details = google_spreadsheet().search_details("gunjan.nandy1@gmail.com")
details = google_spreadsheet().search_details("Gunjan#0010")
print(details)