# Dummy Airflow-style DAG (no external dependency). Illustrative only.
from datetime import datetime
def run():
    print('Order: ingest -> validate -> transform -> annotate -> train_embed_and_anomaly -> evaluate')
    print('Schedule: daily @ 02:00 UTC (example)')
    print(f'Started: {datetime.utcnow().isoformat()}Z')
