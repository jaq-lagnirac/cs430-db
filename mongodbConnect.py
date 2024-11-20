import os
import pprint
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient


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
      #Only used for printing the songs to terminal (TEMP)
      printer = pprint.PrettyPrinter()
      for song in songs:
        printer.pprint(song)
    print("The total number of documents is: ", count)
    return songs
  except:
    print("Something went wrong with the Query:")
    print("1.Did the user answer the questions?")
    print("2.Did the connection string work?")
    
def getAllSongs():
  songs = collection.find()
  allresults = list(songs)
  return allresults

def getSearchFilterQuery(query):
  try:
    songs = collection.find(query)
    count = collection.count_documents(query)
    #Checks if there are songs 
    if count == 0:
      print("We've determined that our dataset does not fit your taste of music. Sadly, we cannot give you any recommendations.")
    else:
      #Only used for printing the songs to terminal (TEMP) 
      printer = pprint.PrettyPrinter()
      for song in songs:
        printer.pprint(song)
    print("The total number of documents is: ", count)
    return songs
  except:
    print("Something went wrong with the Query:")
    print("1.Did the user answer the questions?")
    print("2.Did the connection string work?")
  

#Everything else handles the mongodb connection

#Need to setup a .env where for the connection string
load_dotenv(find_dotenv())
try:
  #Connection to Database
  connection_string = os.environ.get("CONNECTION_STRING")
  client = MongoClient(connection_string)
  #Access the data
  #dbs = client.list_database_names()
  spotify_songs = client.Truify_Discocgraphy_Database
  #collections = spotify_songs.list_collection_names()
  collection  = spotify_songs.Songs
except Exception as e:
  print(e)



  





