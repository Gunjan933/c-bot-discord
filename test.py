from utils.spreadsheet import google_spreadsheet
from utils.database import bot_database

def main():
  sheet = google_spreadsheet()
  database = bot_database()
  # database.sync_database_with_spreadsheet(sheet.get_spreadsheet_dataframe())
  database.print_database()

if __name__=="__main__":
  main()