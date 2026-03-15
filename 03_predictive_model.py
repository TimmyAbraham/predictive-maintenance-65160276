import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ====== INPUT ======
CURRENT_RMS = 2.699  # mm/s (จาก Step 1)
months_back = 6
months_forward = 12

# ISO thresholds for 15–300 kW, Rigid
A_B = 2.8
B_C = 4.5
C_D = 7.1

# ====== Create timeline (months) ======
months = np.arange(-months_back, months_forward + 1)  # e.g. -6 ... +12
t0_idx = np.where(months == 0)[0][0]

# ====== Scenario definitions ======
# 1) Normal wear: slow linear increase
s1_slope = 0.10  # mm/s per month

# 2) Misalignment/Unbalance: medium linear increase
s2_slope = 0.25  # mm/s per month

# 3) Bearing damage: exponential growth
#    choose growth so it crosses C/D within the horizon
growth = 0.10  # 10% per month (tunable)

def scenario_linear(slope):
    return CURRENT_RMS + slope * (months - 0)

def scenario_exponential(g):
    y = np.zeros_like(months, dtype=float)
    y[t0_idx:] = CURRENT_RMS * (1 + g) ** (months[t0_idx:] - 0)
    # back-cast (for completeness)
    y[:t0_idx] = CURRENT_RMS / (1 + g) ** (0 - months[:t0_idx])
    return y

s1 = scenario_linear(s1_slope)
s2 = scenario_linear(s2_slope)
s3 = scenario_exponential(growth)

df = pd.DataFrame({
    "Month_from_now": months,
    "RMS_NormalWear": s1,
    "RMS_Misalignment": s2,
    "RMS_BearingDamage": s3
})

# ====== helper: find crossing month ======
def crossing_month(series, threshold):
    idx = np.where(series >= threshold)[0]
    if len(idx) == 0:
        return None
    return int(months[idx[0]])

def summarize(name, series):
    mC = crossing_month(series, B_C)
    mD = crossing_month(series, C_D)
    return {
        "Scenario": name,
        "Cross_ZoneC(>=4.5)": mC,
        "Cross_ZoneD(>=7.1)": mD
    }

summary = pd.DataFrame([
    summarize("Normal wear (slow)", s1),
    summarize("Misalignment (medium)", s2),
    summarize("Bearing damage (fast)", s3),
])

print("=== STEP 3: PREDICTIVE SUMMARY (months from now) ===")
print(summary.to_string(index=False))

# Save outputs
df.to_csv("step3_simulated_trend.csv", index=False)
summary.to_csv("step3_prediction_summary.csv", index=False)
print("Saved: step3_simulated_trend.csv")
print("Saved: step3_prediction_summary.csv")

# ====== Plot trend ======
plt.figure()
plt.plot(months, s1, label="Normal wear (slow)")
plt.plot(months, s2, label="Misalignment (medium)")
plt.plot(months, s3, label="Bearing damage (fast)")

# Threshold lines
plt.axhline(A_B, linestyle="--", label="ISO A/B (2.8)")
plt.axhline(B_C, linestyle="--", label="ISO B/C (4.5)")
plt.axhline(C_D, linestyle="--", label="ISO C/D (7.1)")

plt.xlabel("Months from now")
plt.ylabel("Velocity RMS (mm/s)")
plt.title("Simulated Velocity RMS Trend + ISO 10816-3 Thresholds (Rigid, 15–300 kW)")
plt.legend()
plt.show()