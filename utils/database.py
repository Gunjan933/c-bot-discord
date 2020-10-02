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
    # try:
    self.form_df = self.form_sheet.get_spreadsheet_dataframe()

    self.database_df = self.df[['Email Address','Project']]

    self.df = pd.merge(self.form_df, self.database_df, how='left', on='Email Address')

    self.df = self.df.rename(columns = {'Discord Username [Ex: Gunjan#0010]':'Discord Username','Medium Username':'Medium URL', 'Timestamp':'Registered on'})
    self.df.fillna('', inplace=True)
    # self.df['Discord Username'] = self.df['Discord Username']
    self.df['Discord Username'] = ("@" + self.df['Discord Username'].str.replace(" ",""))
    self.df.loc[~self.df['Medium URL'].str.contains('https://medium.com/'),'Medium URL'] = ("https://medium.com/" + self.df['Medium URL'])
    self.df.to_json(self.database_name)
    self.database_sheet.update_spreadsheet(self.df)
    return True
    # except:
    #   return False


  def search(self, uniqueID, admin=False):
    if self.df.empty:
      return "No users found with {}".format(uniqueID)
    df = pd.DataFrame(self.df.loc[(self.df['Discord Username'] == "@"+uniqueID)
                        | (self.df['Cainvas Username'] == uniqueID)
                        | (self.df['Email Address'] == uniqueID)
                      ])
    if df.empty:
      return "No users found with {}".format(uniqueID)

    if not admin:
      columns = ['First Name', 'Last Name', 'Email Address',
                'LinkedIn Profile', 'GitHub Profile', 'Medium URL']
      df = df[columns]

    return df.add_suffix(' -  ').T.to_string(header=False).replace("  ","")

  def print_database(self):
    print(self.df)
