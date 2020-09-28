from utils.database import bot_database

def main():
  database = bot_database()
  # database.sync_with_spreadsheet()
  response = database.search("Gunjan#0010", admin=True)
  print(response)
  # print(database.search("Gunjan#0010"))

if __name__=="__main__":
  main()
