import math
import random
import numpy as np
import matplotlib.pyplot as plt


# Dictionary of 20 tourist locations in Rajasthan and their (latitude, longitude)
cities = {
    "Jaipur": (26.91, 75.78),
    "Udaipur": (24.58, 73.68),
    "Jodhpur": (26.23, 73.02),
    "Jaisalmer": (26.91, 70.90),
    "Bikaner": (28.02, 73.31),
    "Pushkar": (26.48, 74.55),
    "Ajmer": (26.44, 74.63),
    "Mount Abu": (24.59, 72.71),
    "Chittorgarh": (24.88, 74.62),
    "Kota": (25.21, 75.83),
    "Bharatpur": (27.21, 77.49),
    "Alwar": (27.55, 76.63),
    "Ranthambore": (25.99, 76.45),
    "Sariska": (27.39, 76.41),
    "Mandawa": (28.05, 75.14),
    "Bundi": (25.44, 75.63),
    "Sikar": (27.61, 75.13),
    "Nagaur": (27.20, 73.74),
    "Shekhawati": (27.85, 75.27),
    "Dungarpur": (23.83, 73.71)
}

# Extract city names and coordinates for easier access
city_names = list(cities.keys())
coordinates = np.array([cities[name] for name in city_names])
num_cities = len(cities)



def calculate_total_distance(tour, coords):
    """Calculates the total Euclidean distance of a tour."""
    total_dist = 0
    for i in range(num_cities):
        # Get coordinates for the current and next city in the tour
        from_city_idx = tour[i]
        to_city_idx = tour[(i + 1) % num_cities] # Use modulo for wrap-around
        
        # Calculate Euclidean distance and add to total
        dist = np.linalg.norm(coords[from_city_idx] - coords[to_city_idx])
        total_dist += dist
    return total_dist


def simulated_annealing(coords, initial_temp, cooling_rate, iterations):
    """
    Solves the TSP using Simulated Annealing.
    
    The core idea is to start with a random solution and iteratively improve it.
    To avoid getting stuck in a local minimum, the algorithm sometimes accepts a
    worse solution with a probability that decreases as the "temperature" cools.
    """
    # Start with a random tour
    current_tour = list(range(num_cities))
    random.shuffle(current_tour)
    current_cost = calculate_total_distance(current_tour, coords)
    
    # Keep track of the best solution found so far
    best_tour = current_tour[:]
    best_cost = current_cost
    
    cost_history = [current_cost]
    temperature = initial_temp
    
    print(f"Initial random tour cost: {current_cost:.2f}")

    for i in range(iterations):
        # Generate a neighbor tour using a "2-opt" swap
        # This is more effective than a simple two-city swap.
        # It picks a sub-section of the tour and reverses it.
        new_tour = current_tour[:]
        l, r = sorted(random.sample(range(num_cities), 2))
        new_tour[l:r+1] = reversed(new_tour[l:r+1])
        
        new_cost = calculate_total_distance(new_tour, coords)
        
        # Decide whether to accept the new tour
        cost_diff = new_cost - current_cost
        
        # Acceptance condition:
        # 1. If the new tour is better, always accept it.
        # 2. If it's worse, accept it with a probability e^(-cost_diff / temperature)
        if cost_diff < 0 or random.random() < math.exp(-cost_diff / temperature):
            current_tour = new_tour[:]
            current_cost = new_cost
        
        # Update the best solution found
        if current_cost < best_cost:
            best_tour = current_tour[:]
            best_cost = current_cost
            
        cost_history.append(best_cost)
        
        # Cool the temperature
        temperature *= cooling_rate
        
        # Optional: Print progress
        if (i + 1) % 10000 == 0:
            print(f"Iteration {i+1}/{iterations} | Best Cost: {best_cost:.2f}")
            
    return best_tour, best_cost, cost_history


def plot_tour(tour, coords, names):
    """Plots the final tour map."""
    plt.figure(figsize=(10, 8))
    
    # Plot lines connecting cities in tour order
    ordered_coords = coords[tour]
    ordered_coords = np.vstack([ordered_coords, ordered_coords[0]]) # Add start point to end to close loop
    
    plt.plot(ordered_coords[:, 1], ordered_coords[:, 0], 'o-', label='Optimized Tour')
    
    # Plot city points and labels
    for i, name in enumerate(names):
        plt.text(coords[i, 1], coords[i, 0], f" {i+1}.{name}", fontsize=9)
    
    plt.title("Optimized Tourist Route for Rajasthan")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_cost_convergence(history):
    """Plots the cost over iterations to show convergence."""
    plt.figure(figsize=(10, 6))
    plt.plot(history)
    plt.title("Cost Convergence Over Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Total Distance (Cost)")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # SA Hyperparameters
    INITIAL_TEMP = 10000.0
    COOLING_RATE = 0.9995  # Slower cooling can yield better results
    ITERATIONS = 100000
    
    # Run the algorithm
    best_tour_indices, best_tour_cost, cost_history = simulated_annealing(
        coordinates, INITIAL_TEMP, COOLING_RATE, ITERATIONS
    )
    
    # --- Print and Plot Results ---
    print("\n" + "="*40)
    print("Optimization Finished!")
    print(f"Final Optimized Tour Cost: {best_tour_cost:.2f}")
    print("="*40)
    
    print("\nOptimized Tour Sequence:")
    for i, city_index in enumerate(best_tour_indices):
        print(f"{i+1}. {city_names[city_index]}")

    # Visualize the results
    plot_tour(best_tour_indices, coordinates, city_names)
    plot_cost_convergence(cost_history)