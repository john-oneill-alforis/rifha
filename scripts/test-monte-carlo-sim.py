import numpy as np
import plotly.graph_objects as go

# Define parameters
num_simulations = 10000
residual_reduction = 0.3

# Define threat details
threats = {
    'SQLi': {
        'probability': 0.6,
        'lower_cost': 100,
        'upper_cost': 10000
    },
    'XSS': {
        'probability': 0.4,
        'lower_cost': 500,
        'upper_cost': 7500
    }
}

# Perform Monte Carlo simulation
simulated_inherent_losses = []
simulated_residual_losses = []
for _ in range(num_simulations):
    inherent_loss = 0
    residual_loss = 0
    for threat, details in threats.items():
        if np.random.uniform() <= details['probability']:
            threat_loss = np.random.uniform(details['lower_cost'], details['upper_cost'])
            inherent_loss += threat_loss
            residual_loss += threat_loss * (1 - residual_reduction)
            simulated_inherent_losses.append(inherent_loss)
            simulated_residual_losses.append(residual_loss)

# Sort the losses in descending order
sorted_inherent_losses = np.sort(simulated_inherent_losses)[::-1]
sorted_residual_losses = np.sort(simulated_residual_losses)[::-1]

# Calculate the exceedance probabilities
exceedance_probs = (np.arange(1, num_simulations + 1) - 0.5) / num_simulations

# Create the loss exceedance curve plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=sorted_inherent_losses, y=exceedance_probs, name='Inherent Loss', mode='lines'))
fig.add_trace(go.Scatter(x=sorted_residual_losses, y=exceedance_probs, name='Residual Loss', mode='lines'))

# Update layout
fig.update_layout(
    title='Loss Exceedance Curve',
    xaxis_title='Loss',
    yaxis_title='Exceedance Probability',
)

# Show the plot
fig.show()
