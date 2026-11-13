"""Airflow DAGs for RAGOps (tested syntax for Airflow 2.10).

DAG 1  ragops_pipeline : ingest -> validate -> preprocess -> feature_engineering -> train -> evaluate -> register
DAG 2  ragops_drift    : check drift hourly; if drift is found, trigger DAG 1 (the loop in the workflow diagram)

Each task just runs one pipeline step with the project's own Python, so Airflow needs no ML libraries.
Set RAGOPS_HOME (project folder) and RAGOPS_PYTHON (e.g. /path/to/project/.venv/bin/python) if not default.
"""
import os
from datetime import datetime
from pathlib import Path

from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from airflow import DAG

HOME = os.getenv("RAGOPS_HOME", str(Path(__file__).resolve().parents[2]))
PY = os.getenv("RAGOPS_PYTHON", f"{HOME}/.venv/bin/python")
ENV = f"cd {HOME} && PYTHONPATH=src:."

STEPS = ["ingest", "validate", "preprocess", "feature_engineering", "train", "evaluate", "register"]

with DAG("ragops_pipeline", start_date=datetime(2026, 1, 1), schedule="@daily", catchup=False,
         tags=["ragops"], default_args={"retries": 0}) as pipeline_dag:
    tasks = [BashOperator(task_id=s, bash_command=f"{ENV} {PY} -m ragops.pipeline --step {s}") for s in STEPS]
    for a, b in zip(tasks, tasks[1:]):
        a >> b


def _drift_found() -> bool:
    import subprocess
    code = subprocess.run(f"{ENV} {PY} monitoring/drift.py", shell=True).returncode
    return code == 1      # drift.py exits with 1 when drift is detected


with DAG("ragops_drift", start_date=datetime(2026, 1, 1), schedule="@hourly", catchup=False,
         tags=["ragops"]) as drift_dag:
    check = ShortCircuitOperator(task_id="check_drift", python_callable=_drift_found)
    retrain = TriggerDagRunOperator(task_id="trigger_retraining", trigger_dag_id="ragops_pipeline")
    check >> retrain
