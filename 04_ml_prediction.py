import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# ===============================
# Load simulated data from Step 3
# ===============================

df = pd.read_csv("step3_simulated_trend.csv")

# ใช้ scenario Misalignment เป็น training example
y = df["RMS_Misalignment"].values
X = np.arange(len(y)).reshape(-1,1)

# ===============================
# Train Polynomial Model
# ===============================

model = make_pipeline(
    PolynomialFeatures(2),
    LinearRegression()
)

model.fit(X, y)

# ===============================
# Predict Future
# ===============================

future_steps = 20
future_X = np.arange(len(y), len(y)+future_steps).reshape(-1,1)

future_pred = model.predict(future_X)

# ===============================
# ISO Threshold
# ===============================

threshold = 7.1

failure_index = None

for i,val in enumerate(future_pred):
    if val >= threshold:
        failure_index = i
        break

# ===============================
# Print Results
# ===============================

print("=== ML Prediction ===")

if failure_index is not None:
    print("Predicted failure in", failure_index, "steps")
else:
    print("No failure predicted")

# ===============================
# Plot
# ===============================

plt.figure(figsize=(10,5))

plt.plot(y,label="Current RMS Trend")
plt.plot(range(len(y),len(y)+future_steps),future_pred,label="ML Forecast")

plt.axhline(2.8,color='green',linestyle='--',label='ISO A/B')
plt.axhline(4.5,color='orange',linestyle='--',label='ISO B/C')
plt.axhline(7.1,color='red',linestyle='--',label='ISO C/D')

plt.xlabel("Samples")
plt.ylabel("Velocity RMS (mm/s)")
plt.title("Machine Learning Forecast (Polynomial Regression)")
plt.legend()

plt.show()