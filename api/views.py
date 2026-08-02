import re

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .db import (
    restaurants_collection,
    reviews_collection,
    is_mongo_available,
    DEFAULT_RESTAURANTS,
    DEFAULT_REVIEWS,
)


def validate_phone(phone_number):
    """Regex for a standard 10-digit phone number."""
    pattern = re.compile(r"^\d{10}$")
    return bool(pattern.match(phone_number))


def validate_pincode(pincode):
    """Regex for a standard 6-digit Indian pincode."""
    pattern = re.compile(r"^[1-9][0-9]{5}$")
    return bool(pattern.match(pincode))


def home(request):
    return Response(
        {
            "message": "FoodieBot API is working!",
            "status": "success",
        }
    )


# ENDPOINT 1: /api/restaurants/
@api_view(["GET", "POST"])
def restaurant_list(request):
    if request.method == "GET":
        search_query = request.GET.get("search", "").lower()

        if is_mongo_available():
            all_restaurants = list(
                restaurants_collection.find({}, {"_id": 0})
            )
        else:
            all_restaurants = list(DEFAULT_RESTAURANTS)

        if search_query:
            filtered_restaurants = [
                r
                for r in all_restaurants
                if search_query in r.get("name", "").lower()
                or search_query in r.get("cuisine", "").lower()
            ]
            return Response(filtered_restaurants)

        return Response(all_restaurants)

    elif request.method == "POST":
        data = request.data

        phone = data.get("phone", "")
        pincode = data.get("pincode", "")

        if not validate_phone(phone):
            return Response(
                {"error": "Invalid 10-digit phone number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not validate_pincode(pincode):
            return Response(
                {"error": "Invalid 6-digit pincode."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_restaurant = {
            "name": data.get("name"),
            "cuisine": data.get("cuisine"),
            "phone": phone,
            "pincode": pincode,
            "menu": data.get("menu", []),  # Stored as an array/tuple
        }

        if is_mongo_available():
            restaurants_collection.insert_one(new_restaurant)
            new_restaurant.pop("_id", None)
        else:
            # Persist to the in-memory store so it shows up in GET results
            DEFAULT_RESTAURANTS.append(new_restaurant)

        return Response(new_restaurant, status=status.HTTP_201_CREATED)


# ENDPOINT 2: /api/restaurants/<restaurant_name>/reviews/
@api_view(["GET", "POST"])
def restaurant_reviews(request, restaurant_name):
    if request.method == "POST":
        data = request.data
        try:
            rating = int(data.get("rating"))
        except (TypeError, ValueError):
            return Response(
                {"error": "Rating must be between 1 and 5."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not (1 <= rating <= 5):
            return Response(
                {"error": "Rating must be between 1 and 5."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        review = {
            "restaurant_name": restaurant_name,  # Link the review to the restaurant
            "reviewer": data.get("reviewer"),
            "rating": rating,
            "text": data.get("text"),
        }

        if is_mongo_available():
            reviews_collection.insert_one(review)
            review.pop("_id", None)
        else:
            DEFAULT_REVIEWS.append(review)

        return Response(review, status=status.HTTP_201_CREATED)

    elif request.method == "GET":
        if is_mongo_available():
            pipeline = [
                {"$match": {"restaurant_name": restaurant_name}},
                {
                    "$group": {
                        "_id": "$restaurant_name",
                        "average_rating": {"$avg": "$rating"},
                        "total_reviews": {"$sum": 1},
                    }
                },
            ]

            agg_result = list(reviews_collection.aggregate(pipeline))

            all_reviews = list(
                reviews_collection.find(
                    {"restaurant_name": restaurant_name}, {"_id": 0}
                )
            )

            stats = (
                agg_result[0]
                if agg_result
                else {"average_rating": 0, "total_reviews": 0}
            )
        else:
            all_reviews = [
                r
                for r in DEFAULT_REVIEWS
                if r.get("restaurant_name") == restaurant_name
            ]

            if all_reviews:
                avg = sum(r["rating"] for r in all_reviews) / len(all_reviews)
                stats = {
                    "average_rating": round(avg, 1),
                    "total_reviews": len(all_reviews),
                }
            else:
                stats = {"average_rating": 0, "total_reviews": 0}

        return Response({"stats": stats, "reviews": all_reviews})

