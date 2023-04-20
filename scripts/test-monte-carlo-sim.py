import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Number of simulations
num_simulations = 1000

# Possible range of losses
min_loss = 10000
max_loss = 500000

# Mean and standard deviation of losses
mean_loss = 250000
std_dev_loss = 100000

# Generate random values for each simulation
losses = np.random.normal(mean_loss, std_dev_loss, num_simulations)

# Calculate total loss for each simulation
total_losses = np.random.uniform(min_loss, max_loss, num_simulations) + losses

# Plot the results
plt.hist(total_losses, bins=50)
plt.title("Monte Carlo Simulation of Cyber Risk")
plt.xlabel("Total Loss")
plt.ylabel("Frequency")
plt.show()
