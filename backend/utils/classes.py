
import math
from datetime import datetime
from .exceptions import InvalidRatingError

class Review:
    def __init__(self, reviewer_name, rating, text):
        # Exception handling for invalid rating
        if not (1 <= rating <= 5):
            raise InvalidRatingError(f"Rating must be between 1 and 5. Received: {rating}")
        
        self.reviewer_name = reviewer_name
        self.rating = rating
        self.text = text
        # Datetime module for review date
        self.date_posted = datetime.now() 

class Restaurant:
    def __init__(self, name, cuisine, menu_items):
        self.name = name
        self.cuisine = cuisine
        # Tuples for menu items (as requested by the requirements)
        self.menu = tuple(menu_items) 
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def get_average_rating(self):
        if not self.reviews:
            return 0
        
        total_score = sum(review.rating for review in self.reviews)
        raw_average = total_score / len(self.reviews)
        
        # Math module used to round up to the nearest single decimal
        return math.ceil(raw_average * 10) / 10.0

class DietAdvisor:
    def __init__(self):
        # A simple dictionary mapping goals to recommended cuisines/foods
        self.diet_plans = {
            "weight_loss": ["Salads", "Grilled Chicken", "Vegan"],
            "muscle_gain": ["Steakhouse", "High Protein", "Sushi"],
            "maintenance": ["Mediterranean", "Balanced Bowls"]
        }

    def get_recommendation(self, goal):
        goal_key = goal.lower().replace(" ", "_")
        return self.diet_plans.get(goal_key, ["General Balanced Diet"])
    