import gspread
import pandas as pd
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

class google_spreadsheet():

  def __init__(self, sheetName):
    self.sheetName = sheetName
    self.googleAPI = 'cainvas-scholar.json'
    self.scope = ['https://www.googleapis.com/auth/drive']
    self.credentials = service_account.Credentials\
                        .from_service_account_file(self.googleAPI)
    self.scopedCreds = self.credentials.with_scopes(self.scope)

  def get_spreadsheet(self):
    while True:
      try:
        gc = gspread.Client(auth=self.scopedCreds)
        gc.session = AuthorizedSession(self.scopedCreds)
        sheet = gc.open(self.sheetName).sheet1
        return sheet
      except:
        print("Authentication error, trying again")
        pass

  def get_spreadsheet_dataframe(self):
    sheet =  self.get_spreadsheet()
    df = pd.DataFrame(sheet.get_all_records()).applymap(str)
    return df

  def update_spreadsheet(self, df=pd.DataFrame()):
    if df.empty:
      return
    while True:
      try:
        gc = gspread.Client(auth=self.scopedCreds)
        gc.session = AuthorizedSession(self.scopedCreds)
        sheet = gc.open(self.sheetName).sheet1
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        break
      except:
        print("Authentication error, trying again")
        pass
