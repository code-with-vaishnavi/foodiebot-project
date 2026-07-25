"use client";
import { useState } from "react";

export default function DietPlan() {
  const [selectedGoal, setSelectedGoal] = useState("");

  const dietRecommendations = {
    push_day: {
      title: "Push Day Macros",
      focus: "High Carb, Moderate Protein (Fuel for Incline Presses)",
      suggestions: ["Grilled Chicken Wraps", "Quinoa Bowls", "Lean Turkey Burgers"],
    },
    pull_day: {
      title: "Pull Day Recovery",
      focus: "High Protein, Moderate Fat (Muscle Repair for Weighted Pull-ups)",
      suggestions: ["Salmon Steaks", "Edamame Salads", "Tuna Sushi Rolls"],
    },
    leg_day: {
      title: "Leg Day Reload",
      focus: "Maximum Carb & Protein Surplus (Heavy Barbell Squat Recovery)",
      suggestions: ["Steak and Sweet Potatoes", "Pasta Bolognese", "Large Protein Smoothies"],
    },
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">DietAdvisor Dashboard</h1>
      <p className="text-gray-600 mb-8">Select your current training split to find restaurant meals that fit your macro plan.</p>

      <div className="flex gap-4 mb-8">
        <button 
          onClick={() => setSelectedGoal("push_day")}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Push Day
        </button>
        <button 
          onClick={() => setSelectedGoal("pull_day")}
          className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
        >
          Pull Day
        </button>
        <button 
          onClick={() => setSelectedGoal("leg_day")}
          className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
        >
          Leg Day
        </button>
      </div>

      {selectedGoal && (
        <div className="p-6 bg-white shadow-lg rounded-xl border border-gray-100">
          <h2 className="text-2xl font-semibold mb-2">
            {dietRecommendations[selectedGoal as keyof typeof dietRecommendations].title}
          </h2>
          <p className="text-gray-500 italic mb-4">
            {dietRecommendations[selectedGoal as keyof typeof dietRecommendations].focus}
          </p>
          <h3 className="text-lg font-medium mb-3">Recommended Restaurant Meals:</h3>
          <ul className="list-disc pl-5 space-y-2">
            {dietRecommendations[selectedGoal as keyof typeof dietRecommendations].suggestions.map((meal, index) => (
              <li key={index} className="text-gray-700">{meal}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}