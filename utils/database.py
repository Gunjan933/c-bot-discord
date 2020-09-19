import sqlite3
import pandas as pd

class bot_database:

  def __init__(self):
    self.database_name = 'cainvas_scholar.db'
    self.table_name = 'scholar'
    # Create sqlite database and cursor
    self.database = sqlite3.connect(self.database_name)


  def sync_database_with_spreadsheet(self, df=pd.DataFrame()):
    if not df.empty:
      df.to_sql(self.table_name, self.database, if_exists='replace', index=False)

  def print_database(self):
    cursor = self.database.execute('SELECT * from {}'.format(self.table_name))
    columns = [description[0] for description in cursor.description]
    print(columns)
    print(cursor.fetchall())

