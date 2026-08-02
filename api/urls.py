from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="api-home"),
    path("restaurants/", views.restaurant_list, name="restaurant-list"),
    path(
        "restaurants/<str:restaurant_name>/reviews/",
        views.restaurant_reviews,
        name="restaurant-reviews",
    ),
]

