import json
import os

def inject_beautified_cells(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Define the new beautified cells
    
    # --- 1.2 Sales Velocity Beautification ---
    # Anchor: "9689c952" (Line 239)
    # We'll insert after this cell
    
    html_sales_velocity = """
<div style="padding: 20px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
    <h3 style="color: #333; margin-top: 0; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;">📈 Sales Velocity & Temporal Resilience</h3>
    <div style="display: flex; gap: 20px; align-items: flex-start;">
        <div style="flex: 1;">
            <p style="color: #666; line-height: 1.6;">
                This visualization tracks the heartbeat of Kenvue's daily revenue. By applying a <b>7-day rolling average</b>, we strip away daily operational noise to reveal the underlying growth trajectory.
            </p>
            <ul style="color: #444; padding-left: 20px;">
                <li><b>Volume Stability:</b> Consistency in daily transactions indicates high brand stickiness and repeatable consumer behavior.</li>
                <li><b>Growth Pacing:</b> The rolling average trendline provides a realistic baseline for supply chain indexing and inventory forecasting.</li>
                <li><b>Volatility Clusters:</b> Significant spikes above the average often correlate with local seasonal triggers or promotional elasticity.</li>
            </ul>
        </div>
        <div style="flex: 0 0 350px; text-align: center; border: 1px solid #eee; padding: 10px; border-radius: 4px; background: #fafafa;">
            <img src="plots/1_sales_velocity.png" style="width: 100%; border-radius: 2px; margin-bottom: 5px;" alt="Sales Velocity">
            <p style="font-size: 11px; color: #888; margin: 0;">Preview: Daily Revenue & Rolling Trends</p>
        </div>
    </div>
    <div style="margin-top: 15px; padding: 10px; background: #f9f9f9; border-left: 4px solid #333; font-style: italic; color: #555;">
        "A stable velocity trendline is the first indicator of a healthy, predictable business model capable of scaling."
    </div>
</div>
"""

    # --- 1.3 Customer Concentration (Pareto) ---
    # Anchor: "ad970d42" (Line 334)
    
    html_pareto = """
<div style="padding: 20px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
    <h3 style="color: #333; margin-top: 0; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;">🎯 Pareto Analysis: The Vital Few</h3>
    <div style="display: flex; gap: 20px; align-items: flex-start;">
        <div style="flex: 1;">
            <p style="color: #666; line-height: 1.6;">
                The <b>80/20 Rule</b> is operationalized here to identify Kenvue's most critical assets: the power purchasers. Understanding the slope of this curve determines our retention strategy.
            </p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; color: #444;">
                <tr style="border-bottom: 1px solid #eee;">
                    <th style="text-align: left; padding: 8px; font-size: 13px;">Metric</th>
                    <th style="text-align: left; padding: 8px; font-size: 13px;">Business Significance</th>
                </tr>
                <tr>
                    <td style="padding: 8px; font-size: 13px;"><b>Curve Inflection</b></td>
                    <td style="padding: 8px; font-size: 13px;">Point where additional customer acquisition yields diminishing revenue returns.</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-size: 13px;"><b>Concentration Risk</b></td>
                    <td style="padding: 8px; font-size: 13px;">Reliance on a small % of customers; necessitates high-touch loyalty tiers.</td>
                </tr>
            </table>
        </div>
        <div style="flex: 0 0 350px; text-align: center; border: 1px solid #eee; padding: 10px; border-radius: 4px; background: #fafafa;">
            <img src="plots/2_pareto_curve.png" style="width: 100%; border-radius: 2px; margin-bottom: 5px;" alt="Pareto Curve">
            <p style="font-size: 11px; color: #888; margin: 0;">Preview: Cumulative Revenue Concentration</p>
        </div>
    </div>
</div>
"""

    # --- 2.2 Model Heatmaps ---
    # Anchor: "2291880a" (Line 420)
    
    html_heatmaps = """
<div style="padding: 20px; background-color: #fcfcfc; border: 1px solid #e0e0e0; border-radius: 8px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
    <h3 style="color: #333; margin-top: 0; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;">🌡️ Predictive Dynamics: Frequency & Recency Heatmaps</h3>
    <div style="display: flex; gap: 15px; margin-bottom: 15px;">
        <div style="flex: 1; text-align: center; background: white; padding: 10px; border: 1px solid #eee; border-radius: 4px;">
            <img src="plots/3_clv_heatmap.png" style="width: 100%; border-radius: 2px;" alt="CLV Heatmap">
            <p style="font-size: 12px; font-weight: bold; color: #333; margin-top: 5px;">Expected Transactions</p>
            <p style="font-size: 11px; color: #777;">Predicts how often a customer with X frequency/Y recency will return.</p>
        </div>
        <div style="flex: 1; text-align: center; background: white; padding: 10px; border: 1px solid #eee; border-radius: 4px;">
            <img src="plots/4_prob_alive.png" style="width: 100%; border-radius: 2px;" alt="Probability Alive">
            <p style="font-size: 12px; font-weight: bold; color: #333; margin-top: 5px;">Probability Alive</p>
            <p style="font-size: 11px; color: #777;">Identifies "Churn Risk" — the cold zones show where customers have likely drifted away.</p>
        </div>
    </div>
    <div style="color: #555; font-size: 14px; line-height: 1.5; background: #fff; padding: 15px; border-radius: 4px; border: 1px solid #eee;">
        <b>Strategic Command:</b> Use the <b>'Top Right'</b> corner of the "Expected Transactions" map to identify your <i>Champions</i>. Use the <b>'Bottom Right'</b> of the "Probability Alive" map to trigger <i>Re-engagement Campaigns</i> before they churn permanently.
    </div>
</div>
"""

    # --- 2.4 Predicted CLV vs Past Spend ---
    # Anchor: Line 510 approx (Cell d497523f?) - Let's look for the title "Predicted 12-Month CLV vs. Past Spend"
    
    html_clv_scatter = """
<div style="padding: 20px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
    <h3 style="color: #333; margin-top: 0; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;">🔮 Future Potential vs. Historical Reality</h3>
    <div style="display: flex; gap: 20px; align-items: flex-start;">
        <div style="flex: 1;">
            <p style="color: #666; line-height: 1.6;">
                This scatter plot is the <b>Truth Map</b> for our CLV model. It pits actual historical spending against our 12-month forward-looking estimate.
            </p>
            <ul style="color: #444; padding-left: 20px;">
                <li><b>Above the Red Line:</b> Customers poised to deliver more value in the next year than they have historically (Growth Opportunities).</li>
                <li><b>Below the Red Line:</b> High-historical payers who are slowing down (At-Risk Premiums).</li>
                <li><b>Linear Alignment:</b> Confirms model calibration and transaction stability.</li>
            </ul>
        </div>
        <div style="flex: 0 0 350px; text-align: center; border: 1px solid #eee; padding: 10px; border-radius: 4px; background: #fafafa;">
            <img src="plots/5_clv_scatter.png" style="width: 100%; border-radius: 2px; margin-bottom: 5px;" alt="CLV Scatter">
            <p style="font-size: 11px; color: #888; margin: 0;">Preview: Predictive Accuracy Scatter</p>
        </div>
    </div>
</div>
"""

    # Helper to create markdown cell
    def create_md(content):
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": [content]
        }

    new_cells = []
    
    # Process the notebook cells
    i = 0
    while i < len(nb['cells']):
        cell = nb['cells'][i]
        new_cells.append(cell)
        
        # 1.2 Sales Velocity Anchor
        if cell.get('id') == "9689c952":
            new_cells.append(create_md(html_sales_velocity))
            
        # 1.3 Pareto Anchor
        elif cell.get('id') == "ad970d42":
            new_cells.append(create_md(html_pareto))
            
        # 2.2 Model Heatmaps Anchor
        elif cell.get('id') == "2291880a":
            # This is the code cell that plots it, so we add the HTML after the plot
            new_cells.append(create_md(html_heatmaps))

        # 2.4 Predicted CLV Anchor
        # Note: In the earlier view_file, line 508 showed a markdown cell describing section 2.4
        # Let's check the ID for the markdown cell starting "### 2.4 Predicted 12-Month CLV vs. Past Spend"
        # From previous tool calls, I'll look for text match in the current cell
        if cell['cell_type'] == 'markdown' and '### 2.4 Predicted 12-Month CLV' in "".join(cell['source']):
             new_cells.append(create_md(html_clv_scatter))

        i += 1

    nb['cells'] = new_cells

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    
    print(f"Boutification of early sections complete in {notebook_path}")

if __name__ == "__main__":
    inject_beautified_cells('/Users/ashok/Documents/CLV/kenvue_analytics_master_project.ipynb')
