"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(false);

  // Function to fetch data from your Django backend
  const fetchRestaurants = async (query = "") => {
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/restaurants/?search=${query}`);
      const data = await response.json();
      setRestaurants(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    setLoading(false);
  };

  // Fetch all restaurants automatically when the page first loads
  useEffect(() => {
    fetchRestaurants();
  }, []);

  // Handle the user clicking the search button
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault(); // Prevents the page from refreshing
    fetchRestaurants(searchQuery);
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-5xl mx-auto">
        
        {/* Header Section */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-extrabold text-orange-600 mb-4">🍔 FoodieBot</h1>
          <p className="text-xl text-gray-600">Find the best restaurants and diet plans.</p>
        </header>

        {/* Search Bar Section */}
        <form onSubmit={handleSearch} className="flex gap-4 justify-center mb-12">
          <input
            type="text"
            placeholder="Search by restaurant name or cuisine..."
            className="w-full max-w-lg px-6 py-3 rounded-lg border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500 text-black"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button
            type="submit"
            className="px-8 py-3 bg-orange-600 text-white font-semibold rounded-lg shadow-md hover:bg-orange-700 transition"
          >
            Search
          </button>
        </form>

        {/* Results Grid Section */}
        {loading ? (
          <p className="text-center text-gray-500 font-medium">Loading restaurants...</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Replace your current map function output with this: */}
{restaurants.map((rest: any, index: number) => (
  <Link href={`/restaurant/${rest.name}`} key={index}>
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 hover:shadow-xl transition duration-300 cursor-pointer">
      <h3 className="text-2xl font-bold text-gray-800 mb-3">{rest.name}</h3>
      <div className="text-gray-600 space-y-2">
        <p><span className="font-semibold text-gray-800">Cuisine:</span> {rest.cuisine}</p>
        <p><span className="font-semibold text-gray-800">Phone:</span> {rest.phone}</p>
        <p><span className="font-semibold text-gray-800">Pincode:</span> {rest.pincode}</p>
      </div>
    </div>
  </Link>
))}

          </div>
        )}
      </div>
    </main>
  );
}