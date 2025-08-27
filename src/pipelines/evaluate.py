import pandas as pd, numpy as np
from src.utils.config import load_config
from src.utils.logging_config import setup_logging

def main():
    cfg = load_config()
    log = setup_logging('evaluate')
    p = cfg.paths

    df = pd.read_parquet(f"{p.processed}/customer_features_scored.parquet")
    # Simple evaluation-style report
    churn_rate = df['churn_label'].mean()
    top_anom = df.sort_values('anomaly_score', ascending=False).head(10)
    print('=== Evaluation Report ===')
    print(f'Rows: {len(df)} | Churn rate (proxy): {churn_rate:.3f}')
    print('Top-10 anomalies (customer_id, anomaly_score):')
    print(top_anom[['customer_id','anomaly_score']].to_string(index=False))

if __name__ == '__main__':
    main()
