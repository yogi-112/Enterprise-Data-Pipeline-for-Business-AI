import pandas as pd
from src.pipelines.transform import build_customer_agg

def test_build_customer_agg_basic():
    customers = pd.DataFrame({'customer_id':[1], 'signup_date':['2024-01-01'], 'region':['EMEA'], 'segment':['SMB']})
    orders = pd.DataFrame({'order_id':[1],'customer_id':[1],'product_id':[1],'quantity':[2],'order_date':['2024-01-10']})
    invoices = pd.DataFrame({'invoice_id':[1],'order_id':[1],'customer_id':[1],'product_id':[1],'quantity':[2],'invoice_date':['2024-01-12'],'status':['PAID']})
    tickets = pd.DataFrame({'ticket_id':[1],'customer_id':[1],'created_at':['2024-01-15'],'resolved_at':['2024-01-16'],'priority':['LOW']})
    feats = build_customer_agg(customers, orders, invoices, tickets)
    assert 'total_orders' in feats.columns
    assert feats.loc[0,'total_orders'] == 1
