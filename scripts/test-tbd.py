import numpy as np
import matplotlib.pyplot as plt

lower_cost = 10000
upper_cost = 50000
probability = 0.3184
num_runs = 50000
simulated_costs = []

for _ in range(num_runs):
    if np.random.rand() <= probability:
        mean = (upper_cost + lower_cost) / 2
        std_dev = (upper_cost - lower_cost) / 6
        cost = np.random.normal(mean, std_dev)
        if cost < lower_cost:
            cost = lower_cost
        elif cost > upper_cost:
            cost = upper_cost
        simulated_costs.append(cost)

simulated_costs.sort(reverse=True)  # Sort the simulated costs in descending order
num_losses = len(simulated_costs)
exceedance_prob = np.arange(1, num_losses + 1) / num_losses

plt.plot(simulated_costs, exceedance_prob)
plt.xlabel("Cost")
plt.ylabel("Exceedance Probability")
plt.title("Loss Exceedance Curve")
plt.grid(True)
plt.show()
