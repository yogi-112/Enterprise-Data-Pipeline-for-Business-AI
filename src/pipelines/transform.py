import pandas as pd, numpy as np
from src.utils.config import load_config
from src.utils.logging_config import setup_logging

def build_customer_agg(customers, orders, invoices, tickets):
    last_order = orders.groupby('customer_id')['order_date'].max().rename('last_order_date')
    total_orders = orders.groupby('customer_id').size().rename('total_orders')
    spend = orders.merge(invoices[['order_id','status']], on='order_id', how='left')
    spend['line_amount'] = spend['quantity'] * 1.0  # price later via product join if needed
    spend_paid = spend[spend['status'].fillna('OPEN') == 'PAID']
    total_spend = spend_paid.groupby('customer_id')['line_amount'].sum().rename('total_spend')
    avg_order_value = (total_spend / total_orders).fillna(0).rename('avg_order_value')

    ticket_ct = tickets.groupby('customer_id').size().rename('ticket_count')
    ticket_prio = pd.get_dummies(tickets[['customer_id','priority']], columns=['priority']).groupby('customer_id').sum()
    features = pd.concat([total_orders, total_spend, avg_order_value, ticket_ct, ticket_prio], axis=1).fillna(0)
    features = customers[['customer_id','signup_date','region','segment']].merge(features, on='customer_id', how='left').fillna(0)

    # Days since last order
    ref_date = pd.to_datetime('2025-08-01')
    features['last_order_date'] = features['customer_id'].map(last_order)
    features['days_since_last_order'] = (ref_date - features['last_order_date']).dt.days.fillna(9999).astype(int)
    features = features.drop(columns=['last_order_date'])

    # One-hot region/segment
    features = pd.get_dummies(features, columns=['region','segment'], drop_first=True)
    return features

def main():
    cfg = load_config()
    log = setup_logging('transform')
    p = cfg.paths

    customers = pd.read_parquet(f"{p.interim}/customers.parquet")
    orders    = pd.read_parquet(f"{p.interim}/orders.parquet")
    invoices  = pd.read_parquet(f"{p.interim}/invoices.parquet")
    tickets   = pd.read_parquet(f"{p.interim}/tickets.parquet")

    features = build_customer_agg(customers, orders, invoices, tickets)
    features.to_parquet(f"{p.processed}/customer_features.parquet")
    log.info(f"Built features: {features.shape[0]} rows, {features.shape[1]} columns.")

if __name__ == '__main__':
    main()
