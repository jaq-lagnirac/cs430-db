import pandas as pd
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

df = pd.read_csv('songs_normalize.csv')

with open('config.json', 'r') as config:
    login = json.load(config)
    uri = login['mongokey']

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["Truify_Discocgraphy_Database"]
collection = db["Songs"]

# Convert the DataFrame to a list of dictionaries
data = df.to_dict("records")

# Insert the data into the MongoDB collection
collection.insert_many(data)
