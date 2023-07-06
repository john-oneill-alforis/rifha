import numpy as np
import matplotlib.pyplot as plt

# Example probabilities and costs
probabilities = [0.2, 0.3238, 0.6124, 0.6954, 0.8524]
costs = [10, 20, 30, 40, 50]

# Sort the probabilities and costs in ascending order of costs
sorted_indices = np.argsort(costs)
sorted_probabilities = np.array(probabilities)[sorted_indices]
sorted_costs = np.array(costs)[sorted_indices]

# Calculate exceedance probabilities
exceedance_probs = 1 - sorted_probabilities

# Plot the cost-exceedance curve with reversed axes
plt.plot(sorted_costs, exceedance_probs, marker="o")
plt.xlabel("Cost")
plt.ylabel("Exceedance Probability")
plt.title("Cost-Exceedance Curve")
plt.grid(True)
plt.show()
