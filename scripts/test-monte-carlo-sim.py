import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Define the ARO figure and cost
aro = 0.3843
cost = 10000

# Define the number of iterations for the simulation
num_iterations = 500

# Generate random samples from a normal distribution
random_samples = np.random.normal(
    aro, 0.1, num_iterations
)  # adjust the standard deviation as needed

# Calculate the total cost for each random sample
total_costs = random_samples * cost

# Plot the histogram of total costs
plt.hist(total_costs, bins=30, edgecolor="black")
plt.xlabel("Total Cost")
plt.ylabel("Frequency")
plt.title("Risk Cost Model")
plt.show()
