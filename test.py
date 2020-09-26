from utils.database import bot_database

def main():
  database = bot_database()
  # database.sync_with_spreadsheet()
  response = database.search("Gunjan#0010")
  # columns = ['First Name', 'Second Name', 'LinkedIn Profile', 'GitHub Profile', 'Email Address']
  # headers = ["{} : ".format(column) for column in columns]
  # response = (df[columns]).T.to_string(header=False)
  # df = df[columns].T
  # df.index.name = None
  # response = (df).to_string(header=False)
  print(response)
  # print(database.search("Gunjan#0010"))

if __name__=="__main__":
  main()
