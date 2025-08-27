import numpy as np, pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from src.utils.config import load_config
from src.utils.logging_config import setup_logging

def synthesize_customers(n, seed):
    rng = np.random.default_rng(seed)
    base_date = np.datetime64('2023-01-01')
    signup_dates = base_date + rng.integers(0, 365, size=n).astype('timedelta64[D]')
    regions = rng.choice(['EMEA','APAC','AMER','DACH'], size=n, p=[0.35,0.25,0.3,0.1])
    segments = rng.choice(['SMB','MID','ENT'], size=n, p=[0.5,0.35,0.15])
    df = pd.DataFrame({
        'customer_id': np.arange(1, n+1),
        'signup_date': signup_dates.astype('datetime64[ns]'),
        'region': regions,
        'segment': segments
    })
    return df

def synthesize_products(n, seed):
    rng = np.random.default_rng(seed+1)
    cats = ['SaaS', 'Support', 'Consulting', 'Hardware']
    df = pd.DataFrame({
        'product_id': np.arange(1, n+1),
        'category': rng.choice(cats, size=n, p=[0.55,0.15,0.2,0.1]),
        'unit_price': rng.normal(100, 40, size=n).clip(10, 500).round(2)
    })
    return df

def synthesize_orders(n, n_customers, n_products, seed):
    rng = np.random.default_rng(seed+2)
    order_dates = pd.to_datetime('2024-01-01') + pd.to_timedelta(rng.integers(0, 365, size=n), unit='D')
    df = pd.DataFrame({
        'order_id': np.arange(1, n+1),
        'customer_id': rng.integers(1, n_customers+1, size=n),
        'product_id': rng.integers(1, n_products+1, size=n),
        'quantity': rng.integers(1, 8, size=n),
        'order_date': order_dates
    })
    return df

def synthesize_invoices(n, orders, seed):
    rng = np.random.default_rng(seed+3)
    idx = rng.choice(orders.index, size=min(n, len(orders)), replace=False)
    sel = orders.loc[idx].copy().reset_index(drop=True)
    sel['invoice_id'] = np.arange(1, len(sel)+1)
    sel['invoice_date'] = sel['order_date'] + pd.to_timedelta(rng.integers(0, 20, size=len(sel)), unit='D')
    sel['status'] = rng.choice(['PAID','OPEN','OVERDUE'], size=len(sel), p=[0.75,0.2,0.05])
    return sel[['invoice_id','order_id','customer_id','product_id','quantity','invoice_date','status']]

def synthesize_tickets(n, n_customers, seed):
    rng = np.random.default_rng(seed+4)
    created = pd.to_datetime('2024-01-01') + pd.to_timedelta(rng.integers(0, 365, size=n), unit='D')
    priorities = rng.choice(['LOW','MED','HIGH'], size=n, p=[0.6,0.3,0.1])
    resolved = created + pd.to_timedelta(rng.integers(0, 30, size=n), unit='D')
    df = pd.DataFrame({
        'ticket_id': np.arange(1, n+1),
        'customer_id': rng.integers(1, n_customers+1, size=n),
        'created_at': created,
        'resolved_at': resolved,
        'priority': priorities
    })
    return df

def main():
    cfg = load_config()
    log = setup_logging('ingest')
    paths = cfg.paths
    for sub in ['raw','interim','processed','models']:
        Path(getattr(paths, sub)).mkdir(parents=True, exist_ok=True)

    customers = synthesize_customers(cfg.n_customers, cfg.seed)
    products  = synthesize_products(cfg.n_products, cfg.seed)
    orders    = synthesize_orders(cfg.n_orders, cfg.n_customers, cfg.n_products, cfg.seed)
    invoices  = synthesize_invoices(cfg.n_invoices, orders, cfg.seed)
    tickets   = synthesize_tickets(cfg.n_tickets, cfg.n_customers, cfg.seed)

    customers.to_parquet(f"{paths.raw}/customers.parquet")
    products.to_parquet(f"{paths.raw}/products.parquet")
    orders.to_parquet(f"{paths.raw}/orders.parquet")
    invoices.to_parquet(f"{paths.raw}/invoices.parquet")
    tickets.to_parquet(f"{paths.raw}/tickets.parquet")

    log.info('Ingested synthetic tables: customers, products, orders, invoices, tickets.')

if __name__ == '__main__':
    main()
