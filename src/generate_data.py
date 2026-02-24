import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_synthetic_data(output_dir='data'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Generate Transactions Data (for CLV & Anomaly)
    np.random.seed(42)
    n_customers = 1000
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    transactions = []
    customer_ids = [f'CUST_{i:04d}' for i in range(n_customers)]
    
    # Assign customer segments (to make CLV realistic)
    customer_traits = {
        cid: {
            'freq_lambda': np.random.gamma(2, 0.5), # transactions per month
            'avg_spend': np.random.normal(50, 15),
            'first_purchase': start_date + timedelta(days=np.random.randint(0, 365))
        } for cid in customer_ids
    }

    for cid, traits in customer_traits.items():
        curr_date = traits['first_purchase']
        while curr_date <= end_date:
            # Add transaction
            amount = max(5, np.random.normal(traits['avg_spend'], traits['avg_spend']*0.2))
            
            # Anomaly injection: 1% chance of a massive bulk purchase
            if np.random.random() < 0.01:
                amount *= 10
            
            transactions.append([cid, curr_date, amount])
            
            # Wait for next purchase
            days_to_next = np.random.exponential(30 / traits['freq_lambda'])
            curr_date += timedelta(days=max(1, int(days_to_next)))

    df_trans = pd.DataFrame(transactions, columns=['customer_id', 'transaction_date', 'amount'])
    df_trans.to_csv(f'{output_dir}/transactions.csv', index=False)
    print(f"Generated {len(df_trans)} transactions.")

    # 2. Generate Marketing Spend Data (for MMM)
    dates = pd.date_range(start_date, end_date, freq='W')
    channels = ['Search', 'Social', 'TV', 'Email']
    
    mmm_data = []
    for d in dates:
        for ch in channels:
            spend = np.random.uniform(1000, 5000)
            # Base response + Spend effect (diminishing returns)
            # Search: High efficiency, Social: Medium, TV: High volume but lag
            eff = {'Search': 0.8, 'Social': 0.5, 'TV': 0.3, 'Email': 0.9}
            conversions = spend * eff[ch] * (1 + 0.2 * np.sin(d.month * (np.pi/6))) # seasonality
            mmm_data.append([d, ch, spend, int(conversions)])

    df_mmm = pd.DataFrame(mmm_data, columns=['date', 'channel', 'spend', 'conversions'])
    df_mmm.to_csv(f'{output_dir}/marketing_spend.csv', index=False)
    print(f"Generated {len(df_mmm)} marketing records.")

if __name__ == "__main__":
    generate_synthetic_data()
