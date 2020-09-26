import pandas as pd
from utils.spreadsheet import google_spreadsheet

class bot_database:

  def __init__(self):
    self.database_name = 'cainvas-scholar-database.json'
    self.form_sheet_name = "Cainvas Scholar Registration (Responses)"
    self.form_sheet = google_spreadsheet(self.form_sheet_name)
    self.database_sheet_name = "Cainvas Scholar Database"
    self.database_sheet = google_spreadsheet(self.database_sheet_name)

    try:
      self.df = pd.read_json(self.database_name)
    except:
      try:
        self.df = self.database_sheet.get_spreadsheet_dataframe()
      except:
        self.df = pd.DataFrame(columns=['Email Address','Project'])


  def sync_with_spreadsheet(self):
    try:
      self.form_df = self.form_sheet.get_spreadsheet_dataframe()

      self.database_df = self.df[['Email Address','Project']]

      self.df = pd.merge(self.form_df, self.database_df, how='left', on='Email Address')

      self.df.to_json(self.database_name)
      self.database_sheet.update_spreadsheet(self.df)
      return True
    except:
      return False


  def search(self, uniqueID, admin=False):
    if self.df.empty:
      return "No users found with {}".format(uniqueID)
    df = self.df.loc[
                (self.df['Discord Username'] == uniqueID) |
                (self.df['Cainvas Username'] == uniqueID) |
                (self.df['Email Address'] == uniqueID)
              ]
    if df.empty:
      return "No users found with {}".format(uniqueID)

    df['Medium Username'] = "https://medium.com/{}".format(df._get_value(0, 'Medium Username'))
    df['Discord Username'] = "<@{}>".format(df._get_value(0, 'Discord Username'))
    df.rename(columns = {'Medium Username':'Medium URL'}, inplace=True)
    df.rename(columns = {'Timestamp':'Registered on'}, inplace=True)

    if admin:
      return df.T.to_string(header=False)
    else:
      columns = ['First Name', 'Second Name', 'Email Address',
                'LinkedIn Profile', 'GitHub Profile', 'Medium URL']
      return (df[columns]).T.to_string(header=False)


  def print_database(self):
    print(self.df)
