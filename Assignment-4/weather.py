# WEATHER DATA VISUALIZER - COMPLETE ASSIGNMENT
# Name: <Your Name>
# Course: Programming for Problem Solving Using Python
# Assignment: Weather Data Visualizer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================================
# TASK 1: LOAD DATA
# ================================

df = pd.read_csv("weather.csv")  # <-- Replace with your actual file name

print("\n=== HEAD OF DATA ===")
print(df.head())

print("\n=== INFO ===")
print(df.info())

print("\n=== DESCRIBE ===")
print(df.describe())

# ================================
# TASK 2: CLEANING DATA
# ================================

# Convert Date → datetime
df['Date'] = pd.to_datetime(df['Date'])

# Drop duplicates
df = df.drop_duplicates()

# Fill missing values
df['Temperature'] = df['Temperature'].fillna(df['Temperature'].mean())
df['Rainfall'] = df['Rainfall'].fillna(0)
df['Humidity'] = df['Humidity'].fillna(df['Humidity'].median())

# Filter important columns
df = df[['Date', 'Temperature', 'Rainfall', 'Humidity']]

# Add Month & Year
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# ================================
# TASK 3: STATISTICAL ANALYSIS (NumPy)
# ================================

daily_mean = np.mean(df['Temperature'])
daily_min = np.min(df['Temperature'])
daily_max = np.max(df['Temperature'])
daily_std = np.std(df['Temperature'])

print("\n=== DAILY TEMPERATURE STATISTICS ===")
print("Mean Temperature:", daily_mean)
print("Min Temperature:", daily_min)
print("Max Temperature:", daily_max)
print("Standard Deviation:", daily_std)

# Monthly statistics
monthly_stats = df.groupby('Month')['Temperature'].agg(['mean', 'min', 'max', 'std'])
print("\n=== MONTHLY STATISTICS ===")
print(monthly_stats)

# ================================
# TASK 4: VISUALIZATION (Matplotlib)
# ================================

# ---- 1. Line Plot (Daily Temperature)
plt.figure(figsize=(10,5))
plt.plot(df['Date'], df['Temperature'])
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.savefig("daily_temperature.png")
plt.show()

# ---- 2. Bar Chart (Monthly Rainfall)
monthly_rainfall = df.groupby('Month')['Rainfall'].sum()

plt.figure(figsize=(10,5))
plt.bar(monthly_rainfall.index, monthly_rainfall.values)
plt.title("Monthly Rainfall")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.savefig("monthly_rainfall.png")
plt.show()

# ---- 3. Scatter Plot (Humidity vs Temperature)
plt.figure(figsize=(7,5))
plt.scatter(df['Temperature'], df['Humidity'])
plt.title("Humidity vs Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.savefig("humidity_vs_temperature.png")
plt.show()

# ---- 4. Combined Subplots (Bonus)
fig, axs = plt.subplots(1, 2, figsize=(12,5))

# Subplot 1
axs[0].plot(df['Date'], df['Temperature'])
axs[0].set_title("Temperature Trend")

# Subplot 2
axs[1].bar(monthly_rainfall.index, monthly_rainfall.values)
axs[1].set_title("Monthly Rainfall")

plt.savefig("combined_plots.png")
plt.show()

# ================================
# TASK 5: GROUPING & AGGREGATION
# ================================

def get_season(month):
    if month in [12,1,2]:
        return "Winter"
    elif month in [3,4,5]:
        return "Summer"
    elif month in [6,7,8]:
        return "Rainy"
    else:
        return "Autumn"

df["Season"] = df["Month"].apply(get_season)

season_stats = df.groupby("Season")['Temperature'].mean()
print("\n=== SEASONAL TEMPERATURE MEAN ===")
print(season_stats)

# ================================
# TASK 6: EXPORT CLEANED DATA + REPORT
# ================================

df.to_csv("cleaned_weather.csv", index=False)
print("\nCleaned CSV exported → cleaned_weather.csv")

# ---- Generate Report
with open("report.md", "w") as f:
    f.write("# Weather Data Visualizer – Summary Report\n\n")
    f.write("## Temperature Insights\n")
    f.write(f"- Average Temperature: {daily_mean:.2f} °C\n")
    f.write(f"- Maximum Temperature: {daily_max:.2f} °C\n")
    f.write(f"- Minimum Temperature: {daily_min:.2f} °C\n")
    f.write(f"- Standard Deviation: {daily_std:.2f}\n\n")
    
    f.write("## Monthly Rainfall\n")
    f.write(str(monthly_rainfall))
    f.write("\n\n## Seasonal Temperature Averages\n")
    f.write(str(season_stats))

print("Report generated → report.md")

print("\n=== ASSIGNMENT COMPLETE ===")