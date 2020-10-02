from utils.database import bot_database

def main():
  database = bot_database()
  # database.sync_with_spreadsheet()
  # response = database.search("aka_trip", admin=True)
  # response = database.search("sauravsolanki#7164")
  response = database.search("hammad.mohammad7860@gmail.com", admin=True)
  print(response)
  # print(database.search("Gunjan#0010"))

if __name__=="__main__":
  main()
