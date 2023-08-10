import numpy as np
import matplotlib.pyplot as plt

# Example records and similarity matrix
records = [
    "This is the first document.",
    "This document is the second document.",
    "And this is the third one.",
    "Is this the first document?"
]
cosine_similarities = np.array([
    [1.0, 0.67, 0.30, 0.82],
    [0.67, 1.0, 0.39, 0.70],
    [0.30, 0.39, 1.0, 0.24],
    [0.82, 0.70, 0.24, 1.0]
])

# Create a heatmap
plt.figure(figsize=(8, 6))
plt.imshow(cosine_similarities, cmap="YlGnBu", interpolation="nearest")
plt.title("Similarity Matrix")
plt.xticks(np.arange(len(records)), records, rotation=45, ha="right")
plt.yticks(np.arange(len(records)), records)
plt.colorbar()
plt.tight_layout()
plt.show()
