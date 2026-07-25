
import requests

# The URL of the API endpoint we built
API_URL = "http://127.0.0.1:8000/api/restaurants/"

# Our dummy database of restaurants
dummy_restaurants = [
    {
        "name": "Mumbai Macro Meals",
        "cuisine": "High Protein",
        "phone": "9876543210",
        "pincode": "400001",
        "menu": ["Grilled Paneer Tikka", "Chicken Breast Bowl", "Quinoa Salad"]
    },
    {
        "name": "Pune Iron Skillet",
        "cuisine": "Steakhouse",
        "phone": "9988776655",
        "pincode": "411001",
        "menu": ["Buffalo Steak", "Sweet Potato Mash", "Grilled Asparagus"]
    },
    {
        "name": "Desi Fit Kitchen",
        "cuisine": "Balanced Bowls",
        "phone": "9123456789",
        "pincode": "400002",
        "menu": ["Dal Makhani (Low Fat)", "Brown Rice Pulao", "Sprout Salad"]
    },
    {
        "name": "The Recovery Room",
        "cuisine": "Vegan",
        "phone": "9876500000",
        "pincode": "422001",
        "menu": ["Plant Protein Shake", "Greek Yogurt Parfait", "Edamame Bowl"]
    }
]

print("Starting data injection...")

# Loop through the list and send each one to the Django API
for rest in dummy_restaurants:
    response = requests.post(API_URL, json=rest)
    
    if response.status_code == 201:
        print(f"✅ Successfully added: {rest['name']}")
    else:
        print(f"❌ Failed to add {rest['name']}: {response.text}")

print("Data injection complete!")