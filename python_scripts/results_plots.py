import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

# Confusion matrix values
TP = 364   # True Positives
FP = 4     # False Positives
FN = 0     # False Negatives
TN = 572832  # True Negatives

# Compute metrics
accuracy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP)
recall = TP / (TP + FN)
f1_score = 2 * (precision * recall) / (precision + recall)
mcc_numerator = (TP * TN) - (FP * FN)
mcc_denominator = sqrt((TP + FP)*(TP + FN)*(TN + FP)*(TN + FN))
mcc = mcc_numerator / mcc_denominator if mcc_denominator else 0

# Labels and values
metrics = ['Accuracy', 'Precision (PPV)', 'Recall (TPR)', 'F1 Score', 'MCC']
values = [accuracy, precision, recall, f1_score, mcc]

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(metrics, values, color='skyblue')
plt.ylim(0.95, 1.01)  # Zoom in since all values are close to 1
plt.title('Performance Metrics at Threshold 1e-6')

# Annotate bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval - 0.005, f'{yval:.4f}', ha='center', va='top')

plt.grid(axis='y')
plt.tight_layout()
plt.show()







