import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FILE_PATH = r"C:\Users\tpkti\Documents\Predictive maintenance\A_Cooling Pump OAH 02_M1H_1480_Oct24.txt"

def parse_waveform_txt(path: str) -> pd.DataFrame:
    """
    Parses the waveform text file where each row contains multiple (Time, Amplitude) pairs.
    Skips the header and returns a tidy DataFrame with columns: Time_ms, Acc_g
    """
    # Data section starts after the dashed header line (in this file it's around line 9)
    raw = pd.read_csv(path, skiprows=8, sep=r"\s+", header=None)

    time_ms, acc_g = [], []
    for _, row in raw.iterrows():
        vals = row.dropna().values
        # Expect pairs: t1 a1 t2 a2 t3 a3 t4 a4 ...
        for i in range(0, len(vals), 2):
            try:
                time_ms.append(float(vals[i]))
                acc_g.append(float(vals[i + 1]))
            except Exception:
                # ignore any malformed trailing values
                pass

    df = pd.DataFrame({"Time_ms": time_ms, "Acc_g": acc_g})
    df = df.sort_values("Time_ms").reset_index(drop=True)

    # Convert time to seconds and ensure unique timestamps
    df["Time_s"] = df["Time_ms"] / 1000.0
    df = df.drop_duplicates(subset=["Time_s"]).reset_index(drop=True)
    return df

def acc_to_velocity_rms(df: pd.DataFrame) -> dict:
    """
    Converts acceleration (g) -> velocity (mm/s) using:
    - DC offset removal on acceleration
    - trapezoidal integration
    - linear detrend on velocity (remove drift)
    Returns computed arrays and summary metrics.
    """
    t = df["Time_s"].to_numpy()
    acc_g = df["Acc_g"].to_numpy()

    # 1) Remove DC offset from acceleration
    acc_g_demean = acc_g - np.mean(acc_g)

    # 2) g -> m/s^2
    acc_m_s2 = acc_g_demean * 9.81

    # 3) Integrate acceleration -> velocity (m/s) with trapezoid rule
    vel_m_s = np.zeros_like(acc_m_s2)
    dt = np.diff(t)
    for i in range(1, len(t)):
        vel_m_s[i] = vel_m_s[i-1] + 0.5 * (acc_m_s2[i] + acc_m_s2[i-1]) * dt[i-1]

    # 4) Remove drift in velocity (linear detrend: v(t)=a*t+b)
    A = np.vstack([t, np.ones_like(t)]).T
    a, b = np.linalg.lstsq(A, vel_m_s, rcond=None)[0]
    vel_m_s_detrended = vel_m_s - (a * t + b)

    # 5) Convert to mm/s and compute RMS
    vel_mm_s = vel_m_s_detrended * 1000.0
    vel_rms = float(np.sqrt(np.mean(vel_mm_s**2)))
    vel_peak = float(np.max(np.abs(vel_mm_s)))

    return {
        "t": t,
        "acc_g": acc_g,
        "acc_g_demean": acc_g_demean,
        "vel_mm_s": vel_mm_s,
        "vel_rms_mm_s": vel_rms,
        "vel_peak_mm_s": vel_peak,
        "acc_mean_g": float(np.mean(acc_g)),
        "acc_rms_g": float(np.sqrt(np.mean(acc_g**2))),
    }

# ---------- Run Step 1 ----------
df = parse_waveform_txt(FILE_PATH)
out = acc_to_velocity_rms(df)

print("=== STEP 1 RESULTS ===")
print(f"Samples: {len(df):,}")
print(f"Duration (s): {df['Time_s'].iloc[-1] - df['Time_s'].iloc[0]:.3f}")
print(f"Acceleration mean (g): {out['acc_mean_g']:.6f}")
print(f"Acceleration RMS (g):  {out['acc_rms_g']:.6f}")
print(f"Velocity RMS (mm/s):   {out['vel_rms_mm_s']:.3f}")
print(f"Velocity Peak (mm/s):  {out['vel_peak_mm_s']:.3f}")

# Save a tidy CSV for later steps
result_df = pd.DataFrame({
    "Time_s": out["t"],
    "Acc_g_raw": out["acc_g"],
    "Acc_g_demean": out["acc_g_demean"],
    "Vel_mm_s": out["vel_mm_s"],
})
result_df.to_csv("step1_velocity_timeseries.csv", index=False)
print("Saved: step1_velocity_timeseries.csv")

# Quick plots (no fancy styling)
plt.figure()
plt.plot(out["t"], out["acc_g"])
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (g)")
plt.title("Raw Acceleration Waveform")
plt.show()

plt.figure()
plt.plot(out["t"], out["vel_mm_s"])
plt.xlabel("Time (s)")
plt.ylabel("Velocity (mm/s)")
plt.title("Velocity after Integration + Detrend")
plt.show()