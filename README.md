# RAGOps: Monitored Knowledge Assistant for Enterprise Support

HR uploads company documents → employees ask questions → answers cite their sources, or say "I could not find this".
Built as an MLOps project: versioned documents/prompts, tracked experiments, automated pipeline, deployment, monitoring.
**Start with [setup.md](setup.md).**

## How it follows the workflow diagram

| Diagram box | Where it is |
|---|---|
| Versioned data | `data/registry.json` (document versions), DVC (`dvc.yaml`), Git, `configs/prompts.yaml` (prompt versions) |
| Validated feature pipeline | `pipeline.ingest → validate → preprocess → feature_engineering` (`src/ragops/pipeline.py`) |
| Automated training DAG | `airflow/dags/ragops_dag.py` (`ragops_pipeline`) |
| MLflow experiments and registry | `pipeline.evaluate` (3 runs: baseline + 2 candidates) and `pipeline.register` (version + alias `production`) |
| FastAPI + Docker deployment | `api/main.py`, `Dockerfile`, `docker-compose.yml` |
| Monitoring and drift detection | `monitoring/` (Prometheus metrics, Grafana dashboard, `drift.py`) |
| Alert or retraining decision | `ragops_drift` DAG: drift found → triggers `ragops_pipeline` again |

## Layout

```
src/ragops/   core code (documents, retrievers, index, generation, pipeline, service, explain)
api/          FastAPI backend          frontend/   Streamlit Cyberpunk UI:
airflow/      DAGs                                 - Employee_Assistant.py (Neural Knowledge Matrix)
configs/      config.yaml, prompts.yaml            - pages/HR_Portal.py (HR & Ops Command Nexus)
monitoring/   metrics, drift, Prom+Graf            - pages/System_Observability.py (Neural Observability)
tests/        unit, pipeline, API tests   cloud/   optional AWS scripts    docs/  model + data cards
```

## Requirement checklist (course template)

1. **Version control**: Git, DVC (`dvc.yaml`), seed 42 (`utils.set_seed`), `requirements.txt` (run `pip freeze > requirements.lock` to lock)
2. **Experiments**: baseline TF-IDF + dense + hybrid logged to MLflow; best registered with version, alias, tags
3. **Airflow DAG**: ingestion, validation, preprocessing, feature engineering, training, evaluation, registration
4. **Deployment**: FastAPI `/ask`, `/health`, schema validation (422), error handling (503/500), Dockerfile + Compose
5. **CI/CD**: `.github/workflows/ci.yml`, tests in `tests/`, Docker build test, quality gate before promotion
6. **Monitoring**: request count, error rate, latency, answered/no-answer distribution, drift, feedback labels, Prometheus + Grafana
7. **Responsible AI**: LIME (`/explain`), `docs/model_card.md`, `docs/data_card.md` (fairness: not applicable, explained there)
8. **Cloud**: `cloud/` (S3, SageMaker training job, CloudWatch via SageMaker logs, `teardown.py`)

## Honest limitations

- Dense/hybrid retrievers need a one-time model download; they could not be run in the sandbox where this was built (TF-IDF path, API, MLflow, drift, upload flow and tests were run).
- The Airflow DAGs and AWS scripts are written but not executed.
- Eval set is small (12 questions) and groundedness is a lexical proxy. Thresholds (`min_score`) for dense/hybrid are starting guesses: tune on your documents.
- HR auth is a shared token (demo only).
