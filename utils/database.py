import pandas as pd
from utils.spreadsheet import google_spreadsheet

class bot_database:

  def __init__(self):
    self.database_name = 'cainvas-scholar-database.json'
    try:
      self.df = pd.read_json(self.database_name)
    except:
      self.df = pd.DataFrame()

    self.form_sheet_name = "Cainvas Scholar Registration (Responses)"
    self.form_sheet = google_spreadsheet(self.form_sheet_name)
    self.database_sheet_name = "Cainvas Scholar Database"
    self.database_sheet = google_spreadsheet(self.database_sheet_name)

  def sync_with_spreadsheet(self):
    self.form_df = self.form_sheet.get_spreadsheet_dataframe()
    self.database_df = self.database_sheet.get_spreadsheet_dataframe()

    print(self.form_df)
    print(self.database_df)

    self.df = pd.merge(self.form_df, self.database_df, on='Email Address', how='left')

    self.df.to_json(self.database_name)
    # self.database_sheet.update_spreadsheet(self.df)


  def search(self, uniqueID):
    empty_df = pd.DataFrame()
    if self.df.empty:
      return empty_df
    df = self.df.loc[
                (self.df['Discord Username'] == uniqueID) |\
                (self.df['Cainvas Username'] == uniqueID) |\
                # (self.df['cAInvas User Name'] == uniqueID) |\
                (self.df['Email Address'] == uniqueID)
              ]
    return df


  def print_database(self):
    print(self.df)
