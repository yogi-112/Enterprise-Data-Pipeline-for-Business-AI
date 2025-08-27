import pandas as pd, numpy as np, json
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from src.utils.config import load_config
from src.infra.db import get_engine
from src.infra.feature_store import init_feature_store, upsert_customer_features
from src.utils.logging_config import setup_logging
from pathlib import Path
import joblib

def main():
    cfg = load_config()
    log = setup_logging('train_embed_and_anomaly')
    p = cfg.paths

    df = pd.read_parquet(f"{p.processed}/customer_features_labeled.parquet")
    id_col = 'customer_id'
    y = df['churn_label']
    X = df.drop(columns=[id_col, 'signup_date', 'churn_label'])

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    pca = PCA(n_components=cfg.modeling.pca_components, random_state=cfg.seed)
    Z = pca.fit_transform(Xs)

    iforest = IsolationForest(
        contamination=cfg.modeling.isolation_forest.contamination,
        n_estimators=cfg.modeling.isolation_forest.n_estimators,
        random_state=cfg.seed
    )
    scores = -iforest.fit_predict(Z)  # 2 for anomaly, 1 for normal → convert to score
    anomaly_score = iforest.decision_function(Z) * -1.0  # higher means more anomalous

    # Persist models
    Path(p.models).mkdir(parents=True, exist_ok=True)
    joblib.dump({'scaler': scaler, 'pca': pca, 'iforest': iforest}, f"{p.models}/tabular_embed_iforest.joblib")    

    # Prepare feature store payload
    out = df[[id_col, 'total_orders','total_spend','avg_order_value','days_since_last_order','churn_label']].copy()
    out['anomaly_score'] = anomaly_score
    # store embedding as JSON for demo
    out['embed_json'] = [json.dumps(list(z)) for z in Z]

    # Write to SQLite feature store
    engine = get_engine(p.feature_db)
    init_feature_store(engine)
    upsert_customer_features(engine, out)

    out.to_parquet(f"{p.processed}/customer_features_scored.parquet")
    log.info('Stored features & embeddings to SQLite and parquet.')

if __name__ == '__main__':
    main()
