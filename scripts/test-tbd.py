import numpy as np
import matplotlib.pyplot as plt

# Define parameters
aro = 0.2  # Annualized Rate of Occurrence
cost_mean = 1000  # Mean of the cost distribution
cost_std = 200  # Standard deviation of the cost distribution
num_iterations = 1000  # Number of Monte Carlo iterations

# Run Monte Carlo simulation
impacts = []
for _ in range(num_iterations):
    # Determine if event occurs based on ARO
    event_occurs = np.random.uniform(0, 1) < aro

    if event_occurs:
        # Generate cost amount based on the cost distribution
        cost = np.random.normal(cost_mean, cost_std)
        impacts.append(cost)
    else:
        impacts.append(0)

# Calculate statistics
mean_impact = np.mean(impacts)
std_impact = np.std(impacts)
percentile_90 = np.percentile(impacts, 90)

# Print results
print("Monte Carlo Simulation Results:")
print(f"Mean Impact: {mean_impact:.2f}")
print(f"Standard Deviation of Impact: {std_impact:.2f}")
print(f"90th Percentile of Impact: {percentile_90:.2f}")

# Plot histogram
plt.hist(impacts, bins=30, edgecolor="black")
plt.xlabel("Impact")
plt.ylabel("Frequency")
plt.title("Monte Carlo Simulation: Impact Distribution")
plt.grid(True)
plt.show()
