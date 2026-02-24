import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes.plotting import plot_frequency_recency_matrix, plot_probability_alive_matrix
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
import os
import warnings

warnings.filterwarnings('ignore')
sns.set(style='whitegrid', palette='muted')

if not os.path.exists('plots'):
    os.makedirs('plots')

# Data Loading
df_trans = pd.read_csv('data/transactions.csv', parse_dates=['transaction_date'])
df_mmm = pd.read_csv('data/marketing_spend.csv', parse_dates=['date'])

# 1. Sales Velocity
daily_sales = df_trans.groupby('transaction_date')['amount'].sum()
plt.figure(figsize=(15, 6))
plt.plot(daily_sales.index, daily_sales.values, alpha=0.3, label='Daily Sales')
plt.plot(daily_sales.index, daily_sales.rolling(7).mean(), color='red', linewidth=2, label='7-Day Trend')
plt.title('Kenvue Consumer Sales Velocity Trend')
plt.savefig('plots/1_sales_velocity.png')
plt.close()

# 2. Pareto Curve
cust_spend = df_trans.groupby('customer_id')['amount'].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 5))
plt.plot(np.arange(len(cust_spend)), cust_spend.cumsum() / cust_spend.sum(), color='blue', linewidth=2)
plt.axhline(0.8, color='grey', linestyle='--', label='80% Revenue Threshold')
plt.title('Pareto Analysis: Customer Concentration')
plt.savefig('plots/2_pareto_curve.png')
plt.close()

# 3. CLV Models
summary = summary_data_from_transaction_data(
    df_trans, 'customer_id', 'transaction_date', 'amount', 
    observation_period_end=df_trans['transaction_date'].max()
)
summary = summary[summary['frequency'] > 0]
bgf = BetaGeoFitter(penalizer_coef=0.1)
bgf.fit(summary['frequency'], summary['recency'], summary['T'])
ggf = GammaGammaFitter(penalizer_coef=0.1)
ggf.fit(summary['frequency'], summary['monetary_value'])
summary['predicted_clv'] = ggf.customer_lifetime_value(
    bgf, summary['frequency'], summary['recency'], summary['T'], summary['monetary_value'],
    time=12, discount_rate=0.01
)

# 4. CLV Heatmaps
plt.figure(figsize=(10, 8))
plot_frequency_recency_matrix(bgf)
plt.savefig('plots/3_clv_heatmap.png')
plt.close()

plt.figure(figsize=(10, 8))
plot_probability_alive_matrix(bgf)
plt.savefig('plots/4_prob_alive.png')
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(summary['monetary_value'], summary['predicted_clv'], alpha=0.5, color='teal')
plt.plot([0, summary['monetary_value'].max()], [0, summary['monetary_value'].max()], color='red', linestyle='--')
plt.savefig('plots/5_clv_scatter.png')
plt.close()

# 5. Anomalies
iso = IsolationForest(contamination=0.01, random_state=42)
iso.fit(df_trans[['amount']])
df_trans['is_anomaly'] = iso.predict(df_trans[['amount']])
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))
sns.histplot(data=df_trans, x='amount', hue='is_anomaly', bins=50, kde=True, ax=ax1)
ax1.set_yscale('log')
sns.boxplot(x='is_anomaly', y='amount', data=df_trans, ax=ax2)
plt.savefig('plots/6_anomalies.png')
plt.close()

# 6. MMM
def apply_adstock(spend, decay=0.6):
    adstocked = np.zeros_like(spend)
    for i in range(len(spend)):
        adstocked[i] = spend[i] + (decay * adstocked[i-1] if i > 0 else 0)
    return adstocked

mmm_pivot = df_mmm.pivot(index='date', columns='channel', values='spend').fillna(0)
target = df_mmm.groupby('date')['conversions'].sum()
for col in mmm_pivot.columns:
    mmm_pivot[col] = apply_adstock(mmm_pivot[col].values)
    mmm_pivot[col] = np.log1p(mmm_pivot[col])
model = LinearRegression()
model.fit(mmm_pivot, target)
roi_data = pd.DataFrame({'Channel': mmm_pivot.columns, 'ROI_Impact': model.coef_})
plt.figure(figsize=(10, 6))
sns.barplot(data=roi_data.sort_values('ROI_Impact', ascending=False), x='ROI_Impact', y='Channel')
plt.savefig('plots/7_mmm_roi.png')
plt.close()

print("All plots saved in plots/ directory.")
