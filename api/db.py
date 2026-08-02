from pymongo import MongoClient
from pymongo.errors import PyMongoError

# MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://vaishi1304_db_user:vaishi1304@cluster0.i4nem8m.mongodb.net/"

# In-memory fallback dataset (mirrors backend/seed_data.py) so the app still
# works when MongoDB Atlas is unreachable (e.g. a paused/free-tier cluster
# or an SSL/TLS incompatibility in the local Python build).
DEFAULT_RESTAURANTS = [
    {
        "name": "Mumbai Macro Meals",
        "cuisine": "High Protein",
        "phone": "9876543210",
        "pincode": "400001",
        "menu": ["Grilled Paneer Tikka", "Chicken Breast Bowl", "Quinoa Salad"],
    },
    {
        "name": "Pune Iron Skillet",
        "cuisine": "Steakhouse",
        "phone": "9988776655",
        "pincode": "411001",
        "menu": ["Buffalo Steak", "Sweet Potato Mash", "Grilled Asparagus"],
    },
    {
        "name": "Desi Fit Kitchen",
        "cuisine": "Balanced Bowls",
        "phone": "9123456789",
        "pincode": "400002",
        "menu": ["Dal Makhani (Low Fat)", "Brown Rice Pulao", "Sprout Salad"],
    },
    {
        "name": "The Recovery Room",
        "cuisine": "Vegan",
        "phone": "9876500000",
        "pincode": "422001",
        "menu": ["Plant Protein Shake", "Greek Yogurt Parfait", "Edamame Bowl"],
    },
]

# In-memory reviews — used only when MongoDB is unavailable.
DEFAULT_REVIEWS = []

# Lazy connection: pymongo only dials the server when a query is made.
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=2000,
    connectTimeoutMS=3000,
    socketTimeoutMS=3000,
)

db = client["foodiebot_db"]
restaurants_collection = db["restaurants"]
reviews_collection = db["reviews"]

# Tri-state availability flag: None = unknown, then True/False (cached).
MONGO_AVAILABLE = None


def is_mongo_available():
    """Return True when MongoDB responds to a ping; cache the result.

    When Atlas is unreachable, this avoids paying the connection-timeout
    cost on every request (the failure is slow, so we only probe once).
    """
    global MONGO_AVAILABLE
    if MONGO_AVAILABLE is None:
        try:
            db.command("ping")
            MONGO_AVAILABLE = True
        except PyMongoError:
            MONGO_AVAILABLE = False
    return MONGO_AVAILABLE

