import pandas as pd, numpy as np
from src.utils.config import load_config
from src.utils.logging_config import setup_logging

def label_churn_proxy(df: pd.DataFrame) -> pd.Series:
    # Heuristic churn label: inactive for > 180 days or zero orders and older signup
    cond = (df['days_since_last_order'] > 180) | ((df['total_orders'] == 0) & (pd.to_datetime('2025-08-01') - pd.to_datetime(df['signup_date'])).dt.days > 180)
    return cond.astype(int)

def main():
    cfg = load_config()
    log = setup_logging('annotate')
    p = cfg.paths

    feats = pd.read_parquet(f"{p.processed}/customer_features.parquet")
    feats['churn_label'] = label_churn_proxy(feats)
    feats.to_parquet(f"{p.processed}/customer_features_labeled.parquet")
    log.info('Annotated churn labels.')

if __name__ == '__main__':
    main()
