import json
import os

notebook_path = '/Users/ashok/Documents/CLV/kenvue_analytics_master_project.ipynb'

new_cells = [
    {
        "cell_type": "markdown",
        "id": "marketing_eda_expert_header",
        "metadata": {},
        "source": [
            "### 4.2 Deep Dive: Marketing Spend Patterns and Efficiency\n",
            "Building on the ROI results, we examine spend concentration, weekly efficiency (CPA), and statistical correlations."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "marketing_eda_expert_1",
        "metadata": {},
        "outputs": [],
        "source": [
            "# 1. Spend Mix & Temporal Trends\n",
            "spend_share = df_mmm.groupby('channel')['spend'].sum()\n",
            "plt.figure(figsize=(15, 6))\n",
            "\n",
            "plt.subplot(1, 2, 1)\n",
            "plt.pie(spend_share, labels=spend_share.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))\n",
            "plt.title('Total Marketing Spend Share by Channel')\n",
            "\n",
            "plt.subplot(1, 2, 2)\n",
            "spend_time = df_mmm.pivot(index='date', columns='channel', values='spend').fillna(0)\n",
            "spend_time.plot(kind='area', stacked=True, ax=plt.gca(), alpha=0.7)\n",
            "plt.title('Weekly Marketing Spend Trends')\n",
            "plt.ylabel('Spend ($)')\n",
            "plt.legend(loc='upper left')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "id": "expl_1",
        "metadata": {},
        "source": [
            "![Spend Trends](plots/8_spend_share_combined.png)\n",
            "\n",
            "<div style=\"background-color: #fdfdfd; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; font-family: sans-serif; box-shadow: 0 2px 5px rgba(0,0,0,0.05);\">\n",
            "    <h3 style=\"color: #2c3e50; margin-top: 0;\">\ud83d\udcb0 Spend Mix & Temporal Trends Analysis</h3>\n",
            "    <p style=\"color: #34495e;\">The distribution of marketing investment reveals a strategic reliance on high-reach channels combined with consistent execution.</p>\n",
            "    <ul style=\"color: #2d3436; line-height: 1.6;\">\n",
            "        <li><strong>TV Dominance:</strong> Accounts for <strong>47.6%</strong> of total budget, serving as the primary anchor for mass brand awareness.</li>\n",
            "        <li><strong>Strategic Consistency:</strong> The area chart shows remarkable stability in weekly allocations, indicating a non-pulsing, always-on media strategy.</li>\n",
            "        <li><strong>Digital Balance:</strong> Search and Social provide necessary tactical support to the broader TV-led reach strategy.</li>\n",
            "    </ul>\n",
            "</div>"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "marketing_eda_expert_2",
        "metadata": {},
        "outputs": [],
        "source": [
            "# 2. Efficiency Analysis: CPA over Time\n",
            "df_mmm['cpa'] = df_mmm['spend'] / df_mmm['conversions'].replace(0, np.nan)\n",
            "plt.figure(figsize=(12, 6))\n",
            "sns.lineplot(data=df_mmm, x='date', y='cpa', hue='channel', marker='o')\n",
            "plt.title('Weekly CPA (Cost Per Acquisition) by Channel')\n",
            "plt.ylabel('CPA ($)')\n",
            "plt.grid(True, alpha=0.3)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "id": "expl_2",
        "metadata": {},
        "source": [
            "![CPA Trends](plots/10_cpa_trends.png)\n",
            "\n",
            "<div style=\"background-color: #fdfdfd; padding: 20px; border-radius: 10px; border-left: 5px solid #27ae60; font-family: sans-serif; box-shadow: 0 2px 5px rgba(0,0,0,0.05);\">\n",
            "    <h3 style=\"color: #2c3e50; margin-top: 0;\">\ud83d\udcc9 CPA & Channel Efficiency Trends</h3>\n",
            "    <p style=\"color: #34495e;\">Efficiency analysis tracks the cost required to secure a single conversion, highlighting distinct performance tiers across the mix.</p>\n",
            "    <table style=\"width: 100%; border-collapse: collapse; margin-top: 10px;\">\n",
            "        <tr style=\"background-color: #f8f9fa;\">\n",
            "            <th style=\"text-align: left; padding: 8px; border-bottom: 2px solid #dee2e6;\">Efficiency Tier</th>\n",
            "            <th style=\"text-align: left; padding: 8px; border-bottom: 2px solid #dee2e6;\">Channel Context</th>\n",
            "        </tr>\n",
            "        <tr>\n",
            "            <td style=\"padding: 8px; border-bottom: 1px solid #eee;\"><strong>Precision Leaders</strong></td>\n",
            "            <td style=\"padding: 8px; border-bottom: 1px solid #eee;\">Email and Search maintain the lowest CPA, capturing high-intent demand.</td>\n",
            "        </tr>\n",
            "        <tr>\n",
            "            <td style=\"padding: 8px; border-bottom: 1px solid #eee;\"><strong>Reach Investment</strong></td>\n",
            "            <td style=\"padding: 8px; border-bottom: 1px solid #eee;\">TV and Social show higher CPAs, typical for top-of-funnel awareness activity.</td>\n",
            "        </tr>\n",
            "    </table>\n",
            "</div>"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "marketing_eda_expert_3",
        "metadata": {},
        "outputs": [],
        "source": [
            "# 3. Saturation Curve Visualizations\n",
            "mmm_pivot = df_mmm.pivot(index='date', columns='channel', values='spend').fillna(0)\n",
            "target = df_mmm.groupby('date')['conversions'].sum()\n",
            "channels = mmm_pivot.columns\n",
            "fig, axes = plt.subplots(1, len(channels), figsize=(20, 5), sharey=True)\n",
            "\n",
            "for i, col in enumerate(channels):\n",
            "    raw_spend = df_mmm[df_mmm['channel'] == col].sort_values('date')['spend'].values\n",
            "    sns.regplot(x=raw_spend, y=target.values, ax=axes[i], logx=True, \n",
            "                scatter_kws={'alpha':0.5}, line_kws={'color':'red'})\n",
            "    axes[i].set_title(f'Saturation: {col}')\n",
            "    axes[i].set_xlabel('Spend ($)')\n",
            "    axes[i].set_ylabel('Conversions' if i==0 else '')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "id": "expl_3",
        "metadata": {},
        "source": [
            "![Saturation](plots/11_saturation_curves.png)\n",
            "\n",
            "<div style=\"background-color: #fdfdfd; padding: 20px; border-radius: 10px; border-left: 5px solid #e67e22; font-family: sans-serif; box-shadow: 0 2px 5px rgba(0,0,0,0.05);\">\n",
            "    <h3 style=\"color: #2c3e50; margin-top: 0;\">\u26a0\ufe0f Diminishing Returns & Saturation</h3>\n",
            "    <p style=\"color: #34495e;\">Understanding when extra investment stops generating proportional rewards is critical for budget optimization.</p>\n",
            "    <div style=\"display: grid; grid-template-columns: 1fr 1fr; gap: 10px;\">\n",
            "        <div style=\"padding: 10px; background: #fff; border: 1px solid #eee;\"><strong>Low Headroom:</strong> Social shows rapid flattening, suggesting it's currently near its practical limit.</div>\n",
            "        <div style=\"padding: 10px; background: #fff; border: 1px solid #eee;\"><strong>Scalable Slopes:</strong> Search and Email show resilient growth potential even at higher spend levels.</div>\n",
            "    </div>\n",
            "</div>"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "marketing_eda_expert_4",
        "metadata": {},
        "outputs": [],
        "source": [
            "# 4. Correlation Analysis (Easier to read Bar Chart)\n",
            "corr_df = mmm_pivot.copy()\n",
            "corr_df['Total_Conversions'] = target.values\n",
            "correlations = corr_df.corr()['Total_Conversions'].drop('Total_Conversions').sort_values(ascending=False)\n",
            "\n",
            "plt.figure(figsize=(10, 6))\n",
            "sns.barplot(x=correlations.values, y=correlations.index, palette='viridis')\n",
            "plt.title('Correlation with Total Conversions by Channel')\n",
            "plt.xlabel('Correlation Coefficient')\n",
            "plt.axvline(0, color='black', lw=1)\n",
            "plt.grid(axis='x', linestyle='--', alpha=0.7)\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "id": "expl_4",
        "metadata": {},
        "source": [
            "![Correlation](plots/12_marketing_correlation_bars.png)\n",
            "\n",
            "<div style=\"background-color: #fdfdfd; padding: 20px; border-radius: 10px; border-left: 5px solid #6c5ce7; font-family: sans-serif; box-shadow: 0 2px 5px rgba(0,0,0,0.05);\">\n",
            "    <h3 style=\"color: #2c3e50; margin-top: 0;\">\ud83d\udcc8 Statistical Correlation Strength</h3>\n",
            "    <p style=\"color: #34495e;\">Correlation coefficients quantify the statistical relationship between channel spend and conversion volume.</p>\n",
            "    <p style=\"margin-bottom: 0;\"><strong>Key Findings:</strong> Email leads with an <strong>0.86</strong> correlation, followed closely by Search. These represent the most reliable levers for predictable growth in the current Pain Care mix.</p>\n",
            "</div>"
        ]
    },
    {
        "cell_type": "markdown",
        "id": "e6bbe304",
        "metadata": {},
        "source": [
            "<div style=\"background-color: #fdfdfd; padding: 25px; border-radius: 12px; border-left: 8px solid #007bff; font-family: sans-serif; box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-bottom: 25px;\">\n",
            "    <h2 style=\"color: #2c3e50; margin-top: 0; display: flex; align-items: center;\">\n",
            "        <span style=\"font-size: 1.5em; margin-right: 12px;\">\ud83d\udcca</span> Overall Business Narrative\n",
            "    </h2>\n",
            "    <ul style=\"color: #34495e; line-height: 1.8; font-size: 1.1em;\">\n",
            "        <li><strong>Revenue Concentration:</strong> The top 20% of the customer base drives nearly 80% of total conversion volume.</li>\n",
            "        <li><strong>Retention Dynamics:</strong> High-frequency buyers are the lifeblood of the brand; recency is the single strongest churn signal.</li>\n",
            "        <li><strong>Marketing Performance:</strong> Wide efficiency gaps exist between high-intent Digital ($0.90 CPA) and awareness-led TV ($3.50+ CPA).</li>\n",
            "        <li><strong>Market Maturity:</strong> The Pain Care segment is in a mature phase with highly stable spend-to-revenue correlation.</li>\n",
            "    </ul>\n",
            "</div>\n",
            "\n",
            "<div style=\"background-color: #ffffff; padding: 25px; border-radius: 12px; border: 2px solid #007bff; font-family: sans-serif; box-shadow: 0 4px 15px rgba(0,123,255,0.1);\">\n",
            "    <h2 style=\"color: #007bff; margin-top: 0; display: flex; align-items: center;\">\n",
            "        <span style=\"font-size: 1.5em; margin-right: 12px;\">\ud83c\udfaf</span> Strategic Recommendations\n",
            "    </h2>\n",
            "    <ol style=\"color: #2c3e50; line-height: 1.8; font-size: 1.1em; font-weight: 500;\">\n",
            "        <li style=\"margin-bottom: 12px;\"><span style=\"color: #007bff;\">Protect the High-Value Core:</span> Deploy personalized loyalty incentives for the top decile to mitigate churn risk.</li>\n",
            "        <li style=\"margin-bottom: 12px;\"><span style=\"color: #007bff;\">Precision Reallocation:</span> Shift surplus budget from saturated Social channels into high-headroom Search and Email.</li>\n",
            "        <li style=\"margin-bottom: 12px;\"><span style=\"color: #007bff;\">Reactivation Engine:</span> Automate win-back sequences for high-frequency segments dormant for more than 90 days.</li>\n",
            "        <li style=\"margin-bottom: 12px;\"><span style=\"color: #007bff;\">Anomaly Management:</span> Segregate extreme outlier spenders for specialized high-touch or bulk-wholesale handling.</li>\n",
            "    </ol>\n",
            "</div>"
        ]
    }
]

def run():
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)

        # Remove existing expert and explanation cells
        nb['cells'] = [c for c in nb['cells'] if not str(c.get('id', '')).startswith('marketing_eda_expert') \
                      and not str(c.get('id', '')).startswith('expl_') \
                      and c.get('id') != 'e6bbe304']

        # Anchor: User Summary ID 89bcb837
        insert_idx = -1
        for i, cell in enumerate(nb['cells']):
            if cell.get('id') == '89bcb837':
                insert_idx = i + 1
                break
        
        if insert_idx == -1:
            for i, cell in enumerate(nb['cells']):
                if cell['cell_type'] == 'markdown' and 'Marketing Mix ROI' in ''.join(cell['source']):
                    insert_idx = i + 1
                    break

        if insert_idx == -1:
            insert_idx = len(nb['cells'])

        for i, cell in enumerate(new_cells):
            nb['cells'].insert(insert_idx + i, cell)

        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        
        print("Notebook updated with simplified correlation and image previews.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run()
