# Enterprise-Data-Pipeline-for-Business-AI

End-to-end, production-style **AI Data Engineering** project focused on **structured enterprise data**:
- **Synthetic business domains**: Customers, Products, Orders, Invoices, Tickets.
- **Data Ops**: Ingestion → Validation → Transformation → Annotation → Feature Store.
- **ML/AI**: Tabular embedding (PCA) for representation learning, **IsolationForest** for anomaly detection, basic churn scoring.
- **Infra**: SQLite demo DB, configurable via YAML, modular code, logging, tests, and an Airflow-like DAG.
- **Deliverables**: Clean Python package, SQL schema, reproducible pipeline, and evaluation reports.

> Designed to mirror tasks in roles like **AI Data Engineer / AI Data Ops / ML Data Engineer** with SAP-style enterprise data.

---

## 🧱 Project Layout

```
AI-Data-Engineer-Advanced/
├─ README.md
├─ requirements.txt
├─ configs/
│  └─ config.yaml
├─ data/
│  ├─ raw/ (generated)
│  ├─ interim/ (generated)
│  ├─ processed/ (generated)
│  └─ models/ (generated)
├─ src/
│  ├─ infra/
│  │  ├─ db.py
│  │  └─ feature_store.py
│  ├─ utils/
│  │  ├─ logging_config.py
│  │  └─ config.py
│  └─ pipelines/
│     ├─ ingest.py
│     ├─ validate.py
│     ├─ transform.py
│     ├─ annotate.py
│     ├─ train_embed_and_anomaly.py
│     └─ evaluate.py
├─ dags/
│  └─ ai_data_engineer_demo_dag.py
├─ tests/
│  └─ test_transform.py
└─ scripts/
   └─ run_all.sh
```

---

## 🚀 Quickstart

```bash
# 1) (Optional) Create a venv
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run end-to-end
bash scripts/run_all.sh
# or step-by-step
python -m src.pipelines.ingest
python -m src.pipelines.validate
python -m src.pipelines.transform
python -m src.pipelines.annotate
python -m src.pipelines.train_embed_and_anomaly
python -m src.pipelines.evaluate
```

Artifacts are written under `data/`:
- `data/raw/*.parquet` – synthetic raw tables
- `data/interim/*.parquet` – validated intermediates
- `data/processed/*.parquet` – features / labels stored here and into SQLite
- `data/models/*` – trained PCA and IsolationForest

---

## 🧪 What this shows (aligned to the JD)

- **Structured business data foundation model (tabular representation):** PCA embeddings capture multi-table signals; easily swappable with TabTransformer or an autoencoder.
- **Data extraction & curation:** Synthetic generation mimics CRM/ERP tables; realistic IDs, datetimes, amounts, currencies, statuses.
- **Pipelines & infra:** Modular ETL with config, logging, and a **feature store** (SQLite) for downstream Data Scientists.
- **Annotation & error analysis:** Rule-based churn proxy, anomaly scores, and explainable KPIs; evaluation report printed to console.
- **Collaboration ready:** Clean interfaces, docstrings, tests, and an **Airflow-style DAG** for orchestration.

---

## 🧰 Config

Edit **`configs/config.yaml`** to change sizes, seeds, and thresholds.

---

## 📈 Extending

- Swap PCA with **TabTransformer** or a **PyTorch AutoEncoder** for richer embeddings.
- Replace SQLite with **SAP HANA**, BigQuery, or Snowflake.
- Plug into **Airflow** or **Prefect**; export features to **Feast**.
- Add Great Expectations for data quality rules (row/field-level tests).
- Add CI with `pytest` and pre-commit hooks.

---

## 📜 License

MIT
