

async function fetchRestaurants(searchQuery) {

    const response = await fetch(`http://127.0.0.1:8000/api/restaurants/?search=${searchQuery}`);
    const data = await response.json();

    console.log("Restaurants Data:", data);
    
}


async function searchRestaurants() {
    const searchInput = document.getElementById('searchInput').value;
    const resultsContainer = document.getElementById('resultsContainer');
    
    
    resultsContainer.innerHTML = '<p>Loading...</p>';

    try {
        
        const response = await fetch(`http://127.0.0.1:8000/api/restaurants/?search=${searchInput}`);
        const data = await response.json();

        
        if (data.length === 0) {
            resultsContainer.innerHTML = '<p>No restaurants found.</p>';
            return;
        }


        resultsContainer.innerHTML = '';

        
        data.forEach(restaurant => {
            const card = document.createElement('div');
            card.className = 'card';
            
            card.innerHTML = `
                <h3>${restaurant.name}</h3>
                <p><strong>Cuisine:</strong> ${restaurant.cuisine}</p>
                <p><strong>Phone:</strong> ${restaurant.phone}</p>
                <p><strong>Pincode:</strong> ${restaurant.pincode}</p>
            `;
            
            resultsContainer.appendChild(card);
        });

    } catch (error) {
        console.error("Error fetching data:", error);
        resultsContainer.innerHTML = '<p style="color: red;">Failed to connect to the backend API. Is Django running?</p>';
    }
}


window.onload = () => {
    searchRestaurants();
};