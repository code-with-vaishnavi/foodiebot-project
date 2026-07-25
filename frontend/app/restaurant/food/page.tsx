"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";

export default function RestaurantReviews() {
  const params = useParams();
  const restaurantName = decodeURIComponent(params.name as string);

  const [reviews, setReviews] = useState([]);
  const [stats, setStats] = useState({ average_rating: 0, total_reviews: 0 });
  const [loading, setLoading] = useState(true);

  // Form State
  const [reviewerName, setReviewerName] = useState("");
  const [rating, setRating] = useState(5);
  const [reviewText, setReviewText] = useState("");

  const fetchReviews = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/restaurants/${restaurantName}/reviews/`);
      const data = await response.json();
      setReviews(data.reviews || []);
      setStats(data.stats || { average_rating: 0, total_reviews: 0 });
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchReviews();
  }, [restaurantName]);

  const submitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/restaurants/${restaurantName}/reviews/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          reviewer: reviewerName,
          rating: rating,
          text: reviewText,
        }),
      });

      if (response.ok) {
        // Clear form and refresh reviews to show the new average!
        setReviewerName("");
        setRating(5);
        setReviewText("");
        fetchReviews(); 
      } else {
        alert("Failed to submit review. Ensure rating is between 1 and 5.");
      }
    } catch (error) {
      console.error("Error submitting review:", error);
    }
  };

  if (loading) return <p className="text-center mt-20 text-gray-500">Loading reviews...</p>;

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header & Stats (MongoDB Aggregate Data) */}
        <div className="bg-white p-8 rounded-xl shadow-md border border-gray-100 mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">{restaurantName}</h1>
          <div className="flex gap-6 text-lg">
            <p className="text-orange-600 font-bold">⭐ {stats.average_rating.toFixed(1)} / 5.0 Average</p>
            <p className="text-gray-500">({stats.total_reviews} Total Reviews)</p>
          </div>
        </div>

        {/* Review Form */}
        <div className="bg-white p-8 rounded-xl shadow-md border border-gray-100 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Leave a Review</h2>
          <form onSubmit={submitReview} className="space-y-4">
            <div>
              <label className="block text-gray-700 font-medium mb-2">Your Name</label>
              <input 
                type="text" 
                required 
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 text-black"
                value={reviewerName} 
                onChange={(e) => setReviewerName(e.target.value)} 
              />
            </div>
            <div>
              <label className="block text-gray-700 font-medium mb-2">Rating (1-5)</label>
              <input 
                type="number" 
                min="1" 
                max="5" 
                required 
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 text-black"
                value={rating} 
                onChange={(e) => setRating(Number(e.target.value))} 
              />
            </div>
            <div>
              <label className="block text-gray-700 font-medium mb-2">Review</label>
              <textarea 
                required 
                rows={3}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 text-black"
                value={reviewText} 
                onChange={(e) => setReviewText(e.target.value)} 
              ></textarea>
            </div>
            <button type="submit" className="px-6 py-2 bg-orange-600 text-white font-semibold rounded-lg hover:bg-orange-700 transition">
              Submit Review
            </button>
          </form>
        </div>

        {/* Display Existing Reviews */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Past Reviews</h2>
          {reviews.length > 0 ? (
            reviews.map((rev: any, index: number) => (
              <div key={index} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <div className="flex justify-between mb-2">
                  <h4 className="font-bold text-gray-800">{rev.reviewer}</h4>
                  <span className="text-orange-500 font-medium">⭐ {rev.rating}/5</span>
                </div>
                <p className="text-gray-600">{rev.text}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-500 italic">No reviews yet. Be the first!</p>
          )}
        </div>
      </div>
    </main>
  );
}