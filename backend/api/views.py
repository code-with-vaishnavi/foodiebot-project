
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .db import restaurants_collection, reviews_collection
from utils.helpers import validate_phone, validate_pincode

# ENDPOINT 1
@api_view(['GET', 'POST'])
def restaurant_list(request):
    if request.method == 'GET':
        
        search_query = request.GET.get('search', '').lower()
        

        all_restaurants = list(restaurants_collection.find({}, {'_id': 0}))


        cuisine_mapping = {}
        for r in all_restaurants:
            cuisine = r.get('cuisine', 'Unknown')
            if cuisine not in cuisine_mapping:
                cuisine_mapping[cuisine] = []
            cuisine_mapping[cuisine].append(r)


        if search_query:
            filtered_restaurants = [
                r for r in all_restaurants 
                if search_query in r.get('name', '').lower() or search_query in r.get('cuisine', '').lower()
            ]
            return Response(filtered_restaurants)
            
        return Response(all_restaurants)

    elif request.method == 'POST':
        data = request.data
        
        
        phone = data.get('phone', '')
        pincode = data.get('pincode', '')

        if not validate_phone(phone):
            return Response({"error": "Invalid 10-digit phone number."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not validate_pincode(pincode):
            return Response({"error": "Invalid 6-digit pincode."}, status=status.HTTP_400_BAD_REQUEST)

        # Insert into MongoDB
        new_restaurant = {
            "name": data.get('name'),
            "cuisine": data.get('cuisine'),
            "phone": phone,
            "pincode": pincode,
            "menu": data.get('menu', []) # Stored as an array/tuple
        }
        restaurants_collection.insert_one(new_restaurant)
        
        
        new_restaurant.pop('_id', None)
        return Response(new_restaurant, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def restaurant_reviews(request, restaurant_name):
    if request.method == 'POST':
        data = request.data
        rating = data.get('rating')
        
        
        if not (1 <= int(rating) <= 5):
            return Response({"error": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)
            
        review = {
            "restaurant_name": restaurant_name, # Link the review to the restaurant
            "reviewer": data.get('reviewer'),
            "rating": int(rating),
            "text": data.get('text')
        }
        reviews_collection.insert_one(review)
        
        review.pop('_id', None)
        return Response(review, status=status.HTTP_201_CREATED)
        
    elif request.method == 'GET':
    
        pipeline = [
            {"$match": {"restaurant_name": restaurant_name}},
            {"$group": {
                "_id": "$restaurant_name", 
                "average_rating": {"$avg": "$rating"},
                "total_reviews": {"$sum": 1}
            }}
        ]
        
        
        agg_result = list(reviews_collection.aggregate(pipeline))
        
        
        all_reviews = list(reviews_collection.find({"restaurant_name": restaurant_name}, {'_id': 0}))
        
        
        stats = agg_result[0] if agg_result else {"average_rating": 0, "total_reviews": 0}
        
        return Response({
            "stats": stats,
            "reviews": all_reviews
        })