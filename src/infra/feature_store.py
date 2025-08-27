from sqlalchemy import text
from sqlalchemy.engine import Engine
import pandas as pd

DDL = {
    "customer_features": '''
        CREATE TABLE IF NOT EXISTS customer_features (
            customer_id INTEGER PRIMARY KEY,
            total_orders INTEGER,
            total_spend REAL,
            avg_order_value REAL,
            days_since_last_order INTEGER,
            churn_label INTEGER,
            anomaly_score REAL,
            embed_json TEXT
        );
    '''
}

def init_feature_store(engine: Engine):
    with engine.begin() as conn:
        for ddl in DDL.values():
            conn.execute(text(ddl))

def upsert_customer_features(engine: Engine, df: pd.DataFrame):
    # Assumes df columns match DDL; embed_json is JSON string
    with engine.begin() as conn:
        df.to_sql("customer_features", conn, if_exists="replace", index=False)
