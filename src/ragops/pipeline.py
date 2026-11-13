"""The ML pipeline. Each step reads/writes files in data/processed so Airflow can run steps separately.

    ingest -> validate -> preprocess -> feature_engineering -> train -> evaluate -> register

Run everything:   python -m ragops.pipeline
Run one step:     python -m ragops.pipeline --step ingest
"""
import argparse
import shutil
import sys

import mlflow
from mlflow.tracking import MlflowClient

from .config import ROOT, load_config
from .documents import clean_text, docs_fingerprint, load_documents, make_chunks, update_registry
from .evaluation import evaluate_index
from .index import Index
from .utils import read_json, set_seed, write_json

STEPS = ["ingest", "validate", "preprocess", "feature_engineering", "train", "evaluate", "register"]


def _p(cfg, name):
    return cfg["paths"]["processed_dir"] / name


# 1. Data ingestion -------------------------------------------------------
def ingest(cfg):
    docs = load_documents(cfg["paths"]["raw_dir"])
    update_registry(docs, cfg["paths"]["registry"])   # assigns document versions
    write_json(_p(cfg, "docs_raw.json"), docs)
    print(f"[ingest] {len(docs)} documents")


# 2. Validation -----------------------------------------------------------
def validate(cfg):
    docs = read_json(_p(cfg, "docs_raw.json"), [])
    problems, seen = [], {}
    if not docs:
        problems.append("no documents found in data/raw")
    for d in docs:
        if len(d["text"].split()) < 20:
            problems.append(f"{d['source']}: too short (<20 words) or unreadable")
        if d["sha256"] in seen:
            problems.append(f"{d['source']}: duplicate of {seen[d['sha256']]}")
        seen[d["sha256"]] = d["source"]
    write_json(_p(cfg, "validation_report.json"), {"n_docs": len(docs), "problems": problems})
    if problems:
        raise ValueError("Validation failed: " + "; ".join(problems))
    print("[validate] OK")


# 3. Preprocessing ----------------------------------------------------------
def preprocess(cfg):
    docs = read_json(_p(cfg, "docs_raw.json"))
    for d in docs:
        d["text"] = clean_text(d["text"])
    write_json(_p(cfg, "docs_clean.json"), docs)
    print("[preprocess] cleaned text")


# 4. Feature engineering: chunking per experiment ----------------------------
def feature_engineering(cfg):
    docs = read_json(_p(cfg, "docs_clean.json"))
    for exp in cfg["experiments"]:
        chunks = make_chunks(docs, exp["chunk_size"], exp["overlap"])
        write_json(_p(cfg, f"chunks_{exp['name']}.json"), chunks)
        print(f"[features] {exp['name']}: {len(chunks)} chunks")


# 5. Training: fit each retriever (baseline + candidates) --------------------
def train(cfg):
    set_seed(cfg["seed"])
    skipped = []
    for exp in cfg["experiments"]:
        chunks = read_json(_p(cfg, f"chunks_{exp['name']}.json"))
        try:
            idx = Index.build(exp, chunks, cfg)
        except ImportError as e:
            print(f"[train] SKIP {exp['name']}: {e} (pip install fastembed)")
            skipped.append(exp["name"])
            continue
        idx.save(cfg["paths"]["candidates_dir"] / exp["name"])
        print(f"[train] fitted {exp['name']}")
    write_json(_p(cfg, "skipped.json"), skipped)


# 6. Evaluation + experiment tracking --------------------------------------
def evaluate(cfg):
    mlflow.set_tracking_uri(cfg["mlflow"]["tracking_uri"])
    mlflow.set_experiment(cfg["mlflow"]["experiment"])
    eval_set = read_json(cfg["paths"]["eval_set"])
    registry = read_json(cfg["paths"]["registry"], {})
    results = []
    for exp in cfg["experiments"]:
        cdir = cfg["paths"]["candidates_dir"] / exp["name"]
        if not (cdir / "meta.json").exists():
            continue
        idx = Index.load(cdir, cfg)
        metrics, rows, reference = evaluate_index(idx, eval_set)
        with mlflow.start_run(run_name=exp["name"]) as run:
            mlflow.log_params({**exp, "seed": cfg["seed"], "n_docs": len(registry),
                               "docs_fingerprint": docs_fingerprint(registry),
                               "dense_model": cfg["dense_model"]})
            mlflow.log_metrics(metrics)
            write_json(_p(cfg, f"eval_{exp['name']}.json"), rows)
            mlflow.log_artifact(str(_p(cfg, f"eval_{exp['name']}.json")))
            mlflow.log_artifacts(str(cdir), artifact_path="index")
            mlflow.log_artifact(str(ROOT / "configs" / "config.yaml"))
            mlflow.log_artifact(str(ROOT / "configs" / "prompts.yaml"))
            run_id = run.info.run_id
        results.append({"name": exp["name"], "run_id": run_id, "metrics": metrics, "reference": reference})
        print(f"[evaluate] {exp['name']}: " + ", ".join(f"{k}={v:.3f}" for k, v in metrics.items()))
    write_json(_p(cfg, "results.json"), results)


# 7. Quality gate + model registration + promotion ---------------------------
def register(cfg) -> bool:
    results = read_json(_p(cfg, "results.json"), [])
    if not results:
        raise RuntimeError("No evaluated candidates")
    best = max(results, key=lambda r: r["metrics"]["selection_score"])
    gate, m = cfg["quality_gate"], best["metrics"]
    passed = m["hit_rate"] >= gate["min_hit_rate"] and m["decision_accuracy"] >= gate["min_decision_accuracy"]
    print(f"[register] best={best['name']} gate_passed={passed}")
    write_json(cfg["paths"]["metrics_file"], {"best": best["name"], "gate_passed": passed, **m})
    if not passed:
        print("[register] quality gate FAILED -> previous production index is kept")
        return False

    registry = read_json(cfg["paths"]["registry"], {})
    fp = docs_fingerprint(registry)
    # Promote: copy winning candidate to the folder served by the API
    src = cfg["paths"]["candidates_dir"] / best["name"]
    meta = read_json(src / "meta.json")
    meta.update(reference=best["reference"], metrics=m, run_id=best["run_id"], index_version=fp,
                docs={k: v["version"] for k, v in registry.items()})
    write_json(src / "meta.json", meta)
    dst = cfg["paths"]["index_dir"]
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    # MLflow Model Registry: version + alias + metadata
    mlflow.set_tracking_uri(cfg["mlflow"]["tracking_uri"])
    client, name = MlflowClient(), cfg["mlflow"]["model_name"]
    try:
        client.create_registered_model(name, description="RAG retriever index served by the FastAPI app")
    except Exception:
        pass  # already exists
    mv = client.create_model_version(name, source=f"runs:/{best['run_id']}/index", run_id=best["run_id"],
                                     tags={"retriever": best["name"], "docs_fingerprint": fp,
                                           "hit_rate": f"{m['hit_rate']:.3f}"})
    client.set_registered_model_alias(name, cfg["mlflow"]["alias"], mv.version)
    print(f"[register] registered {name} v{mv.version} with alias '{cfg['mlflow']['alias']}'")
    return True


# Runner ---------------------------------------------------------------------
def run_all(cfg=None) -> bool:
    cfg = cfg or load_config()
    set_seed(cfg["seed"])
    for step in STEPS[:-1]:
        globals()[step](cfg)
    return register(cfg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", choices=STEPS, help="run a single step (default: all)")
    ap.add_argument("--experiments", help="comma-separated experiment names to run")
    args = ap.parse_args()
    if args.experiments:
        import os
        os.environ["RAGOPS_EXPERIMENTS"] = args.experiments
    cfg = load_config()
    set_seed(cfg["seed"])
    if args.step:
        ok = globals()[args.step](cfg)
        sys.exit(0 if ok is not False else 1)
    sys.exit(0 if run_all(cfg) else 1)


if __name__ == "__main__":
    main()
