import nbformat as nbf
import os

def create_kenvue_notebook():
    nb = nbf.v4.new_notebook()

    # 0. Environment Setup
    nb.cells.append(nbf.v4.new_code_cell(
        "import sys\n"
        "import subprocess\n"
        "import os\n"
        "# Ensure plots directory exists\n"
        "if not os.path.exists('plots'):\n"
        "    os.makedirs('plots')\n"
        "try:\n"
        "    import lifetimes\n"
        "    print('Lifetimes library found.')\n"
        "except ImportError:\n"
        "    print('Installing lifetimes...')\n"
        "    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lifetimes'])\n"
        "    print('Installed! Please Restart Kernel and run all cells.')"
    ))

    # 1. Introduction
    nb.cells.append(nbf.v4.new_markdown_cell("# Kenvue Unified Consumer Growth Engine: MASTER VERSION\n"
        "**Author:** Data Science Candidate\n"
        "**Business Focus:** Senior-level integration of CLV, Anomaly Detection, and Media Mix Modeling.\n\n"
        "This project demonstrates an end-to-end framework for **Kenvue (Consumer Health)** to identify, protect, and optimize their consumer base using advanced probabilistic and statistical models.\n\n"
        "---"))

    # 2. Imports & Setup
    nb.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "from lifetimes import BetaGeoFitter, GammaGammaFitter\n"
        "from lifetimes.utils import summary_data_from_transaction_data\n"
        "from lifetimes.plotting import plot_frequency_recency_matrix, plot_probability_alive_matrix\n"
        "from sklearn.ensemble import IsolationForest\n"
        "from sklearn.linear_model import LinearRegression\n"
        "import warnings\n"
        "warnings.filterwarnings('ignore')\n"
        "sns.set(style='whitegrid', palette='muted')\n"
        "print('Advanced Analytics Environment Fully Operational!')"))

    # 3. Data Loading & Advanced EDA
    nb.cells.append(nbf.v4.new_markdown_cell("## 1. Advanced Exploratory Data Analysis (EDA)\n"
        "### 1.1 Data Loading\n"
        "We load purchase history (`transactions.csv`) and marketing spend/conversions (`marketing_spend.csv`)."))
    nb.cells.append(nbf.v4.new_code_cell("df_trans = pd.read_csv('data/transactions.csv', parse_dates=['transaction_date'])\n"
        "df_mmm = pd.read_csv('data/marketing_spend.csv', parse_dates=['date'])\n\n"
        "print(f'Transactions: {df_trans.shape}')\n"
        "print(f'Marketing Records: {df_mmm.shape}')\n"
        "df_trans.head()"))

    # 1.2 Sales Velocity
    nb.cells.append(nbf.v4.new_markdown_cell("### 1.2 Sales Velocity & Rolling Trends\n"
        "**Technical Observation:** Plotting daily revenue with a 7-day rolling average to see past the noise.\n"
        "**Business Insight:** Helps identify seasonal demand peaks (e.g., flu season for Tylenol) and ensures supply chain readiness."))
    nb.cells.append(nbf.v4.new_code_cell("daily_sales = df_trans.groupby('transaction_date')['amount'].sum()\n"
        "plt.figure(figsize=(15, 6))\n"
        "plt.plot(daily_sales.index, daily_sales.values, alpha=0.3, label='Daily Sales')\n"
        "plt.plot(daily_sales.index, daily_sales.rolling(7).mean(), color='red', linewidth=2, label='7-Day Trend')\n"
        "plt.title('Kenvue Consumer Sales Velocity Trend')\n"
        "plt.legend()\n"
        "plt.savefig('plots/1_sales_velocity.png')\n"
        "plt.show()"))

    # 1.3 Pareto Curve
    nb.cells.append(nbf.v4.new_markdown_cell("### 1.3 Pareto Analysis (The 80/20 Rule)\n"
        "**Technical Observation:** Cumulative revenue vs. cumulative customer base.\n"
        "**Business Insight:** Identifies the 'Super-Consumers' who drive the majority of Kenvue's long-term revenue."))
    nb.cells.append(nbf.v4.new_code_cell("cust_spend = df_trans.groupby('customer_id')['amount'].sum().sort_values(ascending=False)\n"
        "plt.figure(figsize=(10, 5))\n"
        "plt.plot(np.arange(len(cust_spend)), cust_spend.cumsum() / cust_spend.sum(), color='blue', linewidth=2)\n"
        "plt.axhline(0.8, color='grey', linestyle='--', label='80% Revenue Threshold')\n"
        "plt.title('Pareto Analysis: Customer Concentration')\n"
        "plt.ylabel('% of Total Revenue')\n"
        "plt.xlabel('Customer Rank')\n"
        "plt.legend()\n"
        "plt.savefig('plots/2_pareto_curve.png')\n"
        "plt.show()"))

    # 4. Advanced CLV
    nb.cells.append(nbf.v4.new_markdown_cell("## 2. Advanced Predictive Customer Lifetime Value (CLV)\n"
        "### 2.1 The BG/NBD Model (Buy-Till-You-Die)\n"
        "**Concept:** captures frequency and recency to predict churn. It is the modern industry successor to the **Pareto/NBD** model."))
    nb.cells.append(nbf.v4.new_code_cell("summary = summary_data_from_transaction_data(\n"
        "    df_trans, 'customer_id', 'transaction_date', 'amount', \n"
        "    observation_period_end=df_trans['transaction_date'].max()\n"
        ")\n"
        "summary = summary[summary['frequency'] > 0]\n\n"
        "bgf = BetaGeoFitter(penalizer_coef=0.1)\n"
        "bgf.fit(summary['frequency'], summary['recency'], summary['T'])\n\n"
        "ggf = GammaGammaFitter(penalizer_coef=0.1)\n"
        "ggf.fit(summary['frequency'], summary['monetary_value'])\n\n"
        "summary['predicted_clv'] = ggf.customer_lifetime_value(\n"
        "    bgf, summary['frequency'], summary['recency'], summary['T'], summary['monetary_value'],\n"
        "    time=12, discount_rate=0.01\n"
        ")\n"
        "print('Predictive CLV Models Successfully Trained.')"))

    # 2.2 Heatmaps
    nb.cells.append(nbf.v4.new_markdown_cell("### 2.2 Visual Proof: Frequency/Recency Heatmap\n"
        "**How to Read:** Bottom-right is the 'safe zone' (Active users). Top-right is the 'danger zone' (High churn risk)."))
    nb.cells.append(nbf.v4.new_code_cell("plt.figure(figsize=(10, 8))\n"
        "plot_frequency_recency_matrix(bgf)\n"
        "plt.title('Expected Future Transactions (Frequency/Recency Heatmap)')\n"
        "plt.savefig('plots/3_clv_heatmap.png')\n"
        "plt.show()"))

    # 2.3 Probability Alive
    nb.cells.append(nbf.v4.new_markdown_cell("### 2.3 Probability a Customer is Still \"Alive\"\n"
        "**Business Insight:** Allows Kenvue to identify the exact point where a user likely switched to a competitor."))
    nb.cells.append(nbf.v4.new_code_cell("plt.figure(figsize=(10, 8))\n"
        "plot_probability_alive_matrix(bgf)\n"
        "plt.title('Heatmap: Probability of Staying Active')\n"
        "plt.savefig('plots/4_prob_alive.png')\n"
        "plt.show()"))

    # 2.4 Simplified Prediction Plot
    nb.cells.append(nbf.v4.new_markdown_cell("### 2.4 Predicted 12-Month CLV vs. Past Spend\n"
        "**Business Insight:** Customers above the red line are predicted to increase their value to Kenvue over the next year."))
    nb.cells.append(nbf.v4.new_code_cell("plt.figure(figsize=(10, 6))\n"
        "plt.scatter(summary['monetary_value'], summary['predicted_clv'], alpha=0.5, color='teal')\n"
        "plt.plot([0, summary['monetary_value'].max()], [0, summary['monetary_value'].max()], color='red', linestyle='--')\n"
        "plt.title('Historical Value vs. Future Predicted CLV')\n"
        "plt.xlabel('Historical Average Transaction ($)')\n"
        "plt.ylabel('Predicted 12-Month CLV ($)')\n"
        "plt.savefig('plots/5_clv_scatter.png')\n"
        "plt.show()"))

    # 5. Advanced Anomaly Detection
    nb.cells.append(nbf.v4.new_markdown_cell("## 3. Anomaly Detection & Business Protection\n"
        "### 3.1 Isolation Forest Outlier Analysis\n"
        "**Concept:** Flagging bulk-buyers or data entry errors to protect model integrity."))
    nb.cells.append(nbf.v4.new_code_cell("iso = IsolationForest(contamination=0.01, random_state=42)\n"
        "iso.fit(df_trans[['amount']])\n"
        "df_trans['is_anomaly'] = iso.predict(df_trans[['amount']])\n\n"
        "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))\n"
        "sns.histplot(data=df_trans, x='amount', hue='is_anomaly', bins=50, kde=True, ax=ax1)\n"
        "ax1.set_yscale('log')\n"
        "ax1.set_title('Log-Scale Outlier Distribution')\n"
        "sns.boxplot(x='is_anomaly', y='amount', data=df_trans, ax=ax2)\n"
        "ax2.set_xticks([0, 1], ['Outliers', 'Normal'])\n"
        "ax2.set_title('Normal vs. Anomaly Value Comparison')\n"
        "plt.savefig('plots/6_anomalies.png')\n"
        "plt.show()"))

    # 6. Advanced MMM (Adstock, Saturation, Baseline)
    nb.cells.append(nbf.v4.new_markdown_cell("## 4. Advanced Media Mix Modeling (MMM)\n"
        "### 4.1 Marketing ROI with Adstock and Saturation Curves\n"
        "**Terminology Applied:**\n"
        "- **Adstock**: modeling the 'carryover effect' of ads.\n"
        "- **Saturation Curve (Log-transform)**: Modeling diminishing returns on spend.\n"
        "- **Baseline Sales**: Sales achieved without marketing (Intercept)."))
    nb.cells.append(nbf.v4.new_code_cell("def apply_adstock(spend, decay=0.6):\n"
        "    adstocked = np.zeros_like(spend)\n"
        "    for i in range(len(spend)):\n"
        "        adstocked[i] = spend[i] + (decay * adstocked[i-1] if i > 0 else 0)\n"
        "    return adstocked\n\n"
        "mmm_pivot = df_mmm.pivot(index='date', columns='channel', values='spend').fillna(0)\n"
        "target = df_mmm.groupby('date')['conversions'].sum()\n\n"
        "# Apply Advanced Marketing Transformation\n"
        "for col in mmm_pivot.columns:\n"
        "    mmm_pivot[col] = apply_adstock(mmm_pivot[col].values)\n"
        "    mmm_pivot[col] = np.log1p(mmm_pivot[col]) # Diminishing Returns (Saturation)\n\n"
        "model = LinearRegression()\n"
        "model.fit(mmm_pivot, target)\n\n"
        "print(f'Estimated Weekly Baseline Conversions: {model.intercept_:.2f}')\n"
        "roi_data = pd.DataFrame({'Channel': mmm_pivot.columns, 'ROI_Impact': model.coef_})\n"
        "plt.figure(figsize=(10, 6))\n"
        "sns.barplot(data=roi_data.sort_values('ROI_Impact', ascending=False), x='ROI_Impact', y='Channel')\n"
        "plt.title('Media Channel ROI: Impact on Conversions (Adstock + Saturation)')\n"
        "plt.savefig('plots/7_mmm_roi.png')\n"
        "plt.show()"))

    # 7. GenAI Advisor
    nb.cells.append(nbf.v4.new_markdown_cell("## 5. GenAI Digital Growth Advisor\n"
        "**Business Action:** Converting high-dimensional data into low-dimensional strategic recipes."))
    nb.cells.append(nbf.v4.new_code_cell("top_channel = roi_data.loc[roi_data['ROI_Impact'].idxmax(), 'Channel']\n"
        "prompt = f'''\n"
        "PROMPT FOR STRATEGY GENERATION:\n"
        "As a Kenvue Digital Strategy Advisor, analyze these results:\n"
        "- Top ROI Channel: {top_channel}\n"
        "- Baseline Weekly Sales: {model.intercept_:.2f}\n"
        "- High-Value CLV Identified: ${summary['predicted_clv'].mean():.2f}\n\n"
        "Create a 3-point activation plan for the Pain Care Brand Manager.\n"
        "'''\n"
        "print('--- INTERVIEW TIP: SHOW THIS PROMPT ---')\n"
        "print(prompt)"))

    # Write notebook
    with open('kenvue_analytics_master_project.ipynb', 'w') as f:
        nbf.write(nb, f)
    print("Master Notebook created: kenvue_analytics_master_project.ipynb")

if __name__ == "__main__":
    create_kenvue_notebook()
