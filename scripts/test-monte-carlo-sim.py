import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

risk = 0.3
min_loss = 10000
max_loss = 100000
num_iterations = 5000  # Number of iterations

losses = []
for _ in range(num_iterations):
    random_number = random.uniform(0, 1)
    if random_number <= risk:
        loss = random.uniform(min_loss, max_loss)
        losses.append(loss)

losses = np.array(losses)
losses_sorted = np.sort(losses)
num_losses = len(losses_sorted)
exceedance = np.arange(1, num_losses + 1) / num_losses

# Plot the histogram
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.hist(losses, bins=50, density=True, alpha=0.7, color="skyblue")
plt.xlabel("Loss")
plt.ylabel("Frequency")
plt.title("Monte Carlo Simulation - Loss Distribution")

# Plot the probability distribution
plt.subplot(1, 3, 2)
kde = gaussian_kde(losses)
x_vals = np.linspace(min_loss, max_loss, 100)
plt.plot(x_vals, kde(x_vals), color="orange")
plt.xlabel("Loss")
plt.ylabel("Probability Density")
plt.title("Probability Distribution")

# Plot the loss exceedance curve
plt.subplot(1, 3, 3)
plt.plot(losses_sorted, 1 - exceedance, color="green")
plt.xlabel("Loss")
plt.ylabel("Exceedance Probability")
plt.title("Loss Exceedance Curve")

# Adjust the spacing between subplots
plt.tight_layout()

# Display the plot
plt.show()
