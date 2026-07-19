

import threading
import time

def fetch_single_restaurant_reviews(restaurant_name):
    """A mock function to simulate a heavy database or API call."""
    print(f"Starting fetch for {restaurant_name}...")
    time.sleep(2) # Simulating a 2-second delay for the network
    print(f"Finished fetching reviews for {restaurant_name}!")

def fetch_all_reviews_concurrently(restaurant_names):
    """
    REQUIREMENT: Threading for review fetching.
    Spawns a new thread for each restaurant so they all fetch simultaneously.
    """
    threads = []
    

    for name in restaurant_names:
        thread = threading.Thread(target=fetch_single_restaurant_reviews, args=(name,))
        threads.append(thread)
        thread.start()
        

    for thread in threads:
        thread.join()
        
    print("All concurrent review fetching is complete.")