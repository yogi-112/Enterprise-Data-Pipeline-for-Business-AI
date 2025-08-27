import pandas as pd
from src.utils.config import load_config
from src.utils.logging_config import setup_logging

MANDATORY = {
    'customers': ['customer_id','signup_date','region','segment'],
    'products': ['product_id','category','unit_price'],
    'orders': ['order_id','customer_id','product_id','quantity','order_date'],
    'invoices': ['invoice_id','order_id','customer_id','product_id','quantity','invoice_date','status'],
    'tickets': ['ticket_id','customer_id','created_at','resolved_at','priority']
}

def validate_table(df: pd.DataFrame, expected_cols: list) -> pd.DataFrame:
    # Basic schema and null checks; could be extended with Great Expectations
    missing = [c for c in expected_cols if c not in df.columns]
    assert not missing, f"Missing columns: {missing}"
    return df.drop_duplicates()

def main():
    cfg = load_config()
    log = setup_logging('validate')
    p = cfg.paths

    dfs = {}
    for name in MANDATORY:
        df = pd.read_parquet(f"{p.raw}/{name}.parquet")
        dfs[name] = validate_table(df, MANDATORY[name])
        dfs[name].to_parquet(f"{p.interim}/{name}.parquet")
        log.info(f"Validated {name}: {len(dfs[name])} rows.")

if __name__ == '__main__':
    main()
