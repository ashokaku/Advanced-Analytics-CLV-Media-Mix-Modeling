import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure plots directory exists
if not os.path.exists('plots'):
    os.makedirs('plots')

# Set style
sns.set(style='whitegrid', palette='muted')

# Load data
df_mmm = pd.read_csv('data/marketing_spend.csv')

# 1. Total Spend Share (Combined Pie & Trends)
spend_share = df_mmm.groupby('channel')['spend'].sum()
plt.figure(figsize=(15, 6))

plt.subplot(1, 2, 1)
plt.pie(spend_share, labels=spend_share.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Total Marketing Spend Share by Channel')

plt.subplot(1, 2, 2)
spend_time = df_mmm.pivot(index='date', columns='channel', values='spend').fillna(0)
spend_time.plot(kind='area', stacked=True, ax=plt.gca(), alpha=0.7)
plt.title('Weekly Marketing Spend Trends')
plt.ylabel('Spend ($)')
plt.legend(loc='upper left')

plt.tight_layout()
plt.savefig('plots/8_spend_share_combined.png')
plt.close()

# 2. Efficiency Analysis: CPA over Time
df_mmm['cpa'] = df_mmm['spend'] / df_mmm['conversions'].replace(0, np.nan)
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_mmm, x='date', y='cpa', hue='channel', marker='o')
plt.title('Weekly CPA (Cost Per Acquisition) by Channel')
plt.ylabel('CPA ($)')
plt.grid(True, alpha=0.3)
plt.savefig('plots/10_cpa_trends.png')
plt.close()

# 3. Saturation Curves
mmm_pivot = df_mmm.pivot(index='date', columns='channel', values='spend').fillna(0)
target = df_mmm.groupby('date')['conversions'].sum()
channels = mmm_pivot.columns

fig, axes = plt.subplots(1, len(channels), figsize=(20, 5), sharey=True)
for i, col in enumerate(channels):
    raw_spend = df_mmm[df_mmm['channel'] == col].sort_values('date')['spend'].values
    sns.regplot(x=raw_spend, y=target.values, ax=axes[i], logx=True, 
                scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    axes[i].set_title(f'Saturation: {col}')
    axes[i].set_xlabel('Spend ($)')
    axes[i].set_ylabel('Conversions' if i==0 else '')

plt.tight_layout()
plt.savefig('plots/11_saturation_curves.png')
plt.close()

# 4. Easier-to-interpret Correlation Plot: Bar Chart
corr_df = mmm_pivot.copy()
corr_df['Total_Conversions'] = target.values
correlations = corr_df.corr()['Total_Conversions'].drop('Total_Conversions').sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=correlations.values, y=correlations.index, palette='viridis')
plt.title('Correlation with Total Conversions by Channel')
plt.xlabel('Correlation Coefficient')
plt.axvline(0, color='black', lw=1)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('plots/12_marketing_correlation_bars.png')
plt.close()

print("Expert EDA plots updated successfully.")
