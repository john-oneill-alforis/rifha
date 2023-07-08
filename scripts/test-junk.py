import numpy as np



lower = 20
upper = 1000

number = np.random.uniform(0,1)

threat_loss = np.random.lognormal(lower, upper)

print(threat_loss)