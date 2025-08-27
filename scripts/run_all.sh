#!/usr/bin/env bash
set -euo pipefail
python -m src.pipelines.ingest
python -m src.pipelines.validate
python -m src.pipelines.transform
python -m src.pipelines.annotate
python -m src.pipelines.train_embed_and_anomaly
python -m src.pipelines.evaluate
echo '✅ Pipeline finished.'
