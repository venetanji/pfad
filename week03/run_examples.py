"""Run and save time-series example plots from week03_notebook.
This script uses a non-interactive backend (Agg) and writes PNG files to week03/plots/.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Reproducible seed and style
np.random.seed(0)
plt.style.use('seaborn-v0_8-darkgrid')

OUT_DIR = os.path.join(os.path.dirname(__file__), 'plots')
os.makedirs(OUT_DIR, exist_ok=True)

# Generate sample data, in your assignment use your own data
rng = pd.date_range(end=pd.Timestamp.today().normalize(), periods=200, freq='6H')
t = np.arange(len(rng))
data = 1.5 * np.sin(2 * np.pi * t / 24) + 0.6 * np.sin(2 * np.pi * t / 12.4) + 0.2 * np.random.randn(len(t))
df = pd.DataFrame({'height': data}, index=rng)

# 1) Line plot
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(df.index, df['height'], color='tab:blue', linewidth=1)
ax.set_title('Tidal Height — Line Plot')
ax.set_xlabel('time')
ax.set_ylabel('meters')
plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'line_plot.png'))
plt.close(fig)

# 2) Multi-series
df['high'] = df['height'].rolling(3, center=True).max()
df['low'] = df['height'].rolling(3, center=True).min()
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(df.index, df['height'], label='height', color='tab:blue', alpha=0.7, linewidth=1)
ax.plot(df.index, df['high'], label='local high', color='tab:red', linestyle='--', linewidth=1)
ax.plot(df.index, df['low'], label='local low', color='tab:green', linestyle='--', linewidth=1)
ax.legend(loc='upper right')
ax.set_title('Tidal Height — Multi-series')
ax.set_xlabel('time')
ax.set_ylabel('meters')
plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'multi_series.png'))
plt.close(fig)

# 3) Rolling mean
df['rolling_mean'] = df['height'].rolling(window=8, min_periods=1).mean()
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(df.index, df['height'], color='lightgray', label='raw', alpha=0.7)
ax.plot(df.index, df['rolling_mean'], color='tab:purple', label='8-sample rolling mean', linewidth=1.5)
ax.set_title('Tidal Height — Rolling Average')
ax.set_xlabel('time')
ax.set_ylabel('meters')
ax.legend()
plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'rolling_mean.png'))
plt.close(fig)

# 4) Monthly aggregated bar chart
df_month = df['height'].resample('M').mean()
fig, ax = plt.subplots(figsize=(8, 3))
ax.bar(df_month.index.strftime('%Y-%m'), df_month.values, color='tab:cyan')
ax.set_title('Monthly Average Tidal Height')
ax.set_xlabel('month')
ax.set_ylabel('meters')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'monthly_avg.png'))
plt.close(fig)

print('Saved plots to', OUT_DIR)
