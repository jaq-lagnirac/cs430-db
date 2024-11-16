from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import functions as func


def printQuery(query):
  print(query)
  
#Handles the quiz querying
def find_all(querys):  
  try:
    songs = collection.find(querys)
    count = collection.count_documents(querys)
    #Checks if there are songs 
    if count == 0:
      print("We've determined that our dataset does not fit your taste of music. Sadly, we cannot give you any recommendations.")
    else:
      for song in songs:
        printer.pprint(song)
    print("The total number of documents is: ", count)
    return songs
  except:
    print("Something went wrong with the Query:")
    print("1.Did the user answer the questions?")
    
  
#Everything else handles the mongodb connection
'''
Need to setup a .env where: 
  MONGODB_USER is the user for database
  MONGODB_USER_PWD is the password for user
'''
load_dotenv(find_dotenv())
user = os.environ.get("MONGODB_USER")
password = os.environ.get("MONGODB_USER_PWD")

try:
  #Connection to Database
  connection_string = f"mongodb+srv://{user}:{password}@cs430-db.67wen.mongodb.net/"
  client = MongoClient(connection_string)
  #Access the data
  #dbs = client.list_database_names()
  spotify_songs = client.Truify_Discocgraphy_Database
  #collections = spotify_songs.list_collection_names()
  collection  = spotify_songs.Songs
except Exception as e:
  print(e)

#Only used for printing the songs to terminal (TEMP)
printer = pprint.PrettyPrinter()

  





