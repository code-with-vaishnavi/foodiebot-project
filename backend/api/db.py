
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://vaishi1304_db_user:vaishi1304@vaishnavi.w7hqwdp.mongodb.net"

# Connect to the MongoDB cluster
client = MongoClient(MONGO_URI)

db = client['foodiebot_db']

restaurants_collection = db['restaurants']
reviews_collection = db['reviews']

print("MongoDB connected successfully!")