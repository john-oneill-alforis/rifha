import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Define threat probabilities and financial outcomes with upper and lower limits (example data)
threats = [
    {"probability": 0.6, "lower_limit": 7000, "upper_limit": 50000},
    {"probability": 0.3, "lower_limit": 1000, "upper_limit": 12000},
    {"probability": 0.5, "lower_limit": 2000, "upper_limit": 9000},
]

# Set the number of Monte Carlo simulation iterations
numIterations = 10000

inherentProbValue = []
inherentCalculatedLosses = []


randomProbability = np.random.uniform(0, 1, numIterations)

# Generate scenarios and combine financial outcomes for each series
for threat in threats:
    probability = threat["probability"]
    lower_limit = threat["lower_limit"]
    upper_limit = threat["upper_limit"]

    print(probability)
    print(lower_limit)
    print(upper_limit)

    for x in randomProbability:
        if x <= probability:
            mean = (np.log(lower_limit) + np.log(upper_limit)) / 2.0
            std_dv = (np.log(upper_limit) - np.log(lower_limit)) / 3.29

            inherentProbValue.append(x)
            inherentCalculatedLosses.append(np.random.lognormal(mean, std_dv))


residualProbValue = []
residualCalculatedLosses = []
# Generate scenarios and combine financial outcomes for each series
for threat in threats:
    probability = threat["probability"] - (threat["probability"] * 0.5)
    lower_limit = threat["lower_limit"]
    upper_limit = threat["upper_limit"]

    print(probability)
    print(lower_limit)
    print(upper_limit)

    for x in randomProbability:
        if x <= probability:
            mean = (np.log(lower_limit) + np.log(upper_limit)) / 2.0
            std_dv = (np.log(upper_limit) - np.log(lower_limit)) / 3.29

            residualProbValue.append(x)
            residualCalculatedLosses.append(np.random.lognormal(mean, std_dv))


iLec = inherentCalculatedLosses.sort(reverse=True)
rLec = residualCalculatedLosses.sort(reverse=True)


riProbValue = inherentProbValue.sort(reverse=True)
rrProbValue = residualProbValue.sort(reverse=True)


inherentCalculatedLosses.sort()
residualCalculatedLosses.sort()

inherentProbValue.sort()
residualProbValue.sort()


##########################################################################################
# Probability Distribution
##########################################################################################

fig = go.Figure()

fig.add_trace(
    go.Histogram(x=residualCalculatedLosses, name="Residual Probability Distribution")
)
fig.add_trace(
    go.Histogram(x=inherentCalculatedLosses, name="Inherent Probability Distribution")
)


# The two histograms are drawn on top of another
fig.update_layout(barmode="stack")
fig.show()


##########################################################################################
# Probability Curve
##########################################################################################

figPC = go.Figure()

figPC.add_trace(
    go.Scatter(
        x=inherentCalculatedLosses, y=inherentProbValue, mode="lines", name="Inherent"
    )
)
figPC.add_trace(
    go.Scatter(
        x=residualCalculatedLosses,
        y=residualProbValue,
        mode="lines",
        name="Residual Probability",
    )
)

figPC.show()


##########################################################################################
# LEC Curve
##########################################################################################

# Example probabilities and costs
probabilities = inherentProbValue
costs = inherentCalculatedLosses

# Sort the probabilities and costs in ascending order of costs
sorted_indices = np.argsort(costs)
sorted_probabilities = np.array(probabilities)[sorted_indices]
sorted_costs = np.array(costs)[sorted_indices]

print(sorted_costs)

# Calculate exceedance probabilities
exceedance_probs = 1 - sorted_probabilities


# Example probabilities and costs
Rprobabilities = residualProbValue
Rcosts = residualCalculatedLosses

# Sort the probabilities and costs in ascending order of costs
Rsorted_indices = np.argsort(Rcosts)
Rsorted_probabilities = np.array(Rprobabilities)[Rsorted_indices]
Rsorted_costs = np.array(Rcosts)[Rsorted_indices]

# Calculate exceedance probabilities
Rexceedance_probs = 1 - Rsorted_probabilities


figLEC = go.Figure()

figLEC.add_trace(
    go.Scatter(x=Rsorted_costs, y=Rexceedance_probs, mode="lines", name="R")
)

figLEC.add_trace(
    go.Scatter(x=sorted_costs, y=exceedance_probs, mode="lines", name="Inherent")
)


figLEC.show()
