# Setup Guide

The main steps are written for **Linux/macOS**. **Windows (PowerShell) users: use the commands in section 2b** — `make` and `export`
do not exist there. Python 3.10, 3.11 or 3.12 all work. Time needed: ~15 minutes.

## 1. Tools to install

| Tool | Why it is here | Install |
|---|---|---|
| **Python 3.10+** (3.11 recommended) | runs everything | Linux: `sudo apt install python3.11 python3.11-venv` · Windows: python.org or `pyenv-win` |
| **Git** + GitHub account | version control, CI | `sudo apt install git` |
| **DVC** | versions data + model, reproducible pipeline | comes with `requirements-dev.txt` |
| **MLflow** | experiment tracking + model registry | comes with `requirements.txt` |
| **Docker + Docker Compose** | runs API, UI, Prometheus, Grafana together | https://docs.docker.com/engine/install/ |
| **Apache Airflow 2.10** | schedules the pipeline DAG | step 6 (separate virtual env) |
| Gemini API key *(optional)* | nicer written answers | https://aistudio.google.com/apikey |
| AWS account + CLI *(optional)* | cloud extension | https://aws.amazon.com/cli/ |

## 2. Install the project

```bash
cd rag-ops
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt        # API + UI + tests + DVC
cp .env.example .env                       # then edit: set HR_TOKEN (and GEMINI_API_KEY if you have one)
git init && git add . && git commit -m "RAGOps MVP"
dvc init && git commit -am "init dvc"      # DVC is now tracking the pipeline in dvc.yaml
```

## 2b. Windows (PowerShell) quick path

The **venv** is created once, inside the project folder. The **Makefile** is only a list of shortcuts and needs nothing installed;
on Windows just run the commands it contains:

```powershell
cd D:\My_Projects\rag-ops
python -m venv venv
.\venv\Scripts\Activate.ps1          # if blocked: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
pip install -r requirements-dev.txt
copy .env.example .env               # then edit .env: set HR_TOKEN (and GEMINI_API_KEY if you have one)

# Terminal 1: build the index  (add the next line first if the embedding model download fails)
# $env:RAGOPS_EXPERIMENTS = "baseline_tfidf"
$env:PYTHONPATH = "src;."
python -m ragops.pipeline

# Terminal 2: backend -> http://localhost:8000/docs      (activate venv + set PYTHONPATH again)
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src;."
uvicorn api.main:app --reload --port 8000

# Terminal 3: frontend -> http://localhost:8501          (activate venv first)
.\venv\Scripts\Activate.ps1
streamlit run frontend/Employee_Assistant.py

# Extras
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000     # MLflow UI
pytest -q                                                         # tests
```
`$env:PYTHONPATH` only lasts for the current terminal, so set it in every terminal that runs Python code from this project
(not needed for `streamlit` or `mlflow ui`). Airflow does not run natively on Windows: use WSL2, or skip it and run the pipeline directly.
In section 4, replace `export A=b` with `$env:A = "b"`.

## 3. Run it on Linux/macOS (3 terminals, `source .venv/bin/activate` in each)

```bash
make pipeline     # 1) builds the index from data/raw, logs 3 experiments to MLflow, registers the best
make api          # 2) backend  -> http://localhost:8000/docs
make ui           # 3) frontend -> http://localhost:8501
```
`make pipeline` prints one line per step. The first run downloads the small embedding model (~130 MB). No internet for it? Run
`RAGOPS_EXPERIMENTS=baseline_tfidf make pipeline` to use the TF-IDF baseline only.

**Using the app**
- **Employee page** (default): type a question → answer + sources. 👍/👎 sends feedback, "Why this answer?" shows the LIME explanation.
- **HR Portal** (sidebar): enter the HR token (default `hr-demo`), upload PDF/MD/TXT files → the pipeline re-runs automatically
  (validate → chunk → index → evaluate → quality gate → promote). Re-uploading a file with the same name bumps its version.
- Try it: ask "How many days of annual leave do I get?", then "What is the capital of Australia?" (it should refuse).

## 4. Each tool, in one minute

**MLflow** – `make mlflow` → http://localhost:5000. Experiment `ragops` shows one run per retriever (parameters, metrics,
the index as artifact). *Models* tab → `ragops-retriever` with versions and the alias `production`.

**DVC** – `dvc repro` runs the pipeline only if documents/code/config changed; hashes go to `dvc.lock`, metrics to `data/metrics.json`.
`dvc metrics show` prints them; `dvc metrics diff` compares with the last commit. For a remote: `dvc remote add -d s3remote s3://YOUR_BUCKET/dvc && dvc push`.

**Docker** – `docker compose up --build` starts API :8000, UI :8501, MLflow :5000, Prometheus :9090, Grafana :3000.
Run `make pipeline` once first so `data/index` exists (or upload documents on the HR page). Stop with `docker compose down`.

**Prometheus / Grafana** – Grafana http://localhost:3000 (login admin/admin) → Dashboards → RAGOps → *RAGOps Monitoring*.
Panels: request rate, error rate, p95 latency, answered vs no-answer, groundedness, top retrieval score, feedback, drift.
Raw metrics: http://localhost:8000/metrics/. Drift check: `curl localhost:8000/drift`
(needs ≥10 recent questions; it compares them with the training-time reference).

**Airflow** – install in its own environment so it does not clash with the project:
```bash
python3.11 -m venv .venv-airflow && source .venv-airflow/bin/activate
pip install "apache-airflow==2.10.5" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.11.txt"
export AIRFLOW_HOME=$(pwd)/airflow AIRFLOW__CORE__LOAD_EXAMPLES=False RAGOPS_PYTHON=$(pwd)/.venv/bin/python
airflow standalone          # prints an admin password; UI at http://localhost:8080
```
Un-pause `ragops_pipeline` (7 tasks) and click ▶ to run it. `ragops_drift` runs hourly and triggers the pipeline if drift is found.

**Tests / CI** – `make test` and `make lint`. On every push GitHub Actions lints, runs the pipeline (the quality gate fails the build
if hit-rate < 75%), runs unit + API tests, and builds the Docker image. Create a GitHub repo and push:
`git remote add origin https://github.com/<you>/rag-ops.git && git push -u origin main`.

## 5. Optional: AWS (S3 + SageMaker + CloudWatch)

```bash
pip install boto3 sagemaker && aws configure
export S3_BUCKET=your-unique-bucket SAGEMAKER_ROLE=arn:aws:iam::<account>:role/<sagemaker-role>
aws s3 mb s3://$S3_BUCKET
python cloud/s3_sync.py upload          # data + index to S3
python cloud/sagemaker_train.py         # pipeline as a SageMaker training job; logs go to CloudWatch
python cloud/teardown.py                # REMOVE resources after the demo (and `aws s3 rb s3://$S3_BUCKET`)
```
These scripts follow the AWS APIs but were **not tested on a real account**; expect to adjust the role/permissions.
Training jobs bill by the second and stop by themselves (`max_run` = 30 min); S3 and endpoints keep costing until deleted.

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| UI says "No index yet" / `/health` shows `no_index` | run `make pipeline` or upload documents on the HR page |
| `ModuleNotFoundError: ragops` or `api` | set `PYTHONPATH` (`export PYTHONPATH=src:.` or PowerShell `$env:PYTHONPATH = "src;."`) in that terminal |
| `make` is not recognized (Windows) | not an error: use section 2b, no installation needed |
| Dense candidates skipped | `pip install fastembed`, check internet for the first model download |
| Quality gate failed after an upload | the old index stays live. Check `data/processed/eval_*.json`, add more/clearer documents, or tune `quality_gate` / `min_score` in `configs/config.yaml` |
| 401 on HR page | the sidebar token must equal `HR_TOKEN` in `.env` |
| Answers are just copied text | no `GEMINI_API_KEY` set (extractive mode) |
