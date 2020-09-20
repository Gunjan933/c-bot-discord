from utils.database import bot_database

def main():
  database = bot_database()
  # database.print_database()
  database.sync_with_spreadsheet()
  database.print_database()
  df = database.search("Gunjan#0010")
  print(df)
  # print(database.search("ashishgoswami8956230@gmail.com"))

if __name__=="__main__":
  main()