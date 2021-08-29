import mysql.connector
from mysql.connector import errorcode
import config
import csv
import pandas as pd

db_config = {
  'user': config.DB_USER,
  'password': config.DB_PWD,
  'host': 'localhost',
  'database': 'SEWordSim-r1',
  'raise_on_warnings': True,
  'auth_plugin': 'mysql_native_password'
}

try:
  cnx = mysql.connector.connect(**db_config)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()

# function to execute sql query and print results to csv
def expQueryResults(query, name):
  cursor.execute(query)
  results = cursor.fetchall()
  df = pd.DataFrame(results)
  df.to_csv(name+'.csv', index=False, header=False)

def printQryResults(query):
  cursor.execute(query)
  results = cursor.fetchall()
  if len(results)>1:
    for row in results:
      print(row)
  else:
    print(results)

query2 = "SELECT count(*) FROM `SEWordSim-r1`.Word_Similarity"

# Find synset with term1 having length > 5
query3 = ("SELECT term1, count(term2) "
            "FROM `SEWordSim-r1`.Word_Similarity "
            "GROUP BY term1 "
            # "HAVING length(term1) >= 5 "
            "ORDER BY term1 DESC")

# Find synset by term1 keyword
query4 = "SELECT term1, term2 FROM `SEWordSim-r1`.Word_Similarity WHERE term1 like 'xcode'"

printQryResults(query2)
# expQueryResults(query3, 'synset_count_full')
expQueryResults(query4, 'synset_xcode') 

cursor.close()
cnx.close()