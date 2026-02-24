# Kenvue Advanced Analytics: CLV & Media Mix Modeling

This project provides a comprehensive data science suite for **Customer Lifetime Value (CLV)** prediction, **Anomaly Detection**, and **Strategic Media Mix Modeling (MMM)**. It is designed to transform raw transaction and marketing spend data into actionable growth strategies.

## 🚀 Key Features

### 1. Customer Lifetime Value (CLV)
- **BG/NBD Model**: Predicts transaction frequency and probability of churn.
- **Gamma-Gamma Model**: Estimates future monetary value of customer cohorts.
- **Predictive Heatmaps**: Visualizes customer "Probability Alive" vs. "Expected Transactions".

### 2. Marketing Media Mix Modeling (MMM)
- **Adstock Transformation**: Scales spend to account for carryover effects and temporal decay.
- **Saturation Analysis**: Uses log-transformation to identify diminishing returns across channels (Search, Email, TV, Social).
- **Efficiency Index**: Calculates CPA (Cost Per Acquisition) trends and ROI per channel.

### 3. Smart Anomaly Detection
- **Isolation Forest**: Automatically flags high-volatility revenue spikes and outliers to distinguish noise from genuine seasonal trends.

### 4. High-End Presentation
- **Professional HTML Cards**: The notebook features a high-end visual overhaul with structured insights and "Strategic Command" callouts.
- **Embedded Visuals**: Over 12+ premium visualizations are saved locally and embedded directly into the report.

---

## 📁 Project Structure

- `kenvue_analytics_master_project.ipynb`: The primary, beautified master notebook containing the full analysis.
- `plots/`: Directory containing all generated PNG visualizations (Sales Velocity, Pareto Curves, Saturation Map, etc.).
- `data/`: CSV datasets for marketing spend and customer transactions.
- `scripts/`: Python utilities used for notebook injection and visual maintenance.

---

## 🛠️ Tech Stack

- **Data Processing**: `pandas`, `numpy`
- **Predictive Modeling**: `lifetimes`, `scikit-learn`
- **Visualization**: `matplotlib`, `seaborn`, `IPython.display`
- **Strategic Layer**: Custom-built HTML/CSS presentation logic within Jupyter.

---

## 📊 Getting Started

1. **Environment Setup**: Ensure you have Python 3.8+ installed.
2. **Dependencies**:
   ```bash
   pip install pandas numpy scikit-learn lifetimes matplotlib seaborn
   ```
3. **Execution**: Open `kenvue_analytics_master_project.ipynb` in your preferred Jupyter environment (VS Code, JupyterLab, etc.) and run all cells.

## 🤖 GenAI Digital Growth Advisor
The notebook includes a pre-configured prompt module designed for LLMs (like Gemini or GPT-4). By feeding the results found in the Strategy Recommendations section into the advisor, you can generate real-time tactical budget reallocations and campaign optimization briefs.

---
**Prepared for Kenvue Analytics**  
*Driving growth through predictive resilience.*
