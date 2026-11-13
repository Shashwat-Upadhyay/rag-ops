"""Simple drift check: compare recent live queries with the reference stats stored at training time.

We log only numbers per query (never the question text): query length, top retrieval score, answered?
Drift here means: employees ask things the documents no longer cover (more refusals, weaker matches)."""
import numpy as np

from ragops.utils import read_json


def read_recent(log_path, window: int) -> list[dict]:
    if not log_path.exists():
        return []
    import json
    lines = log_path.read_text().strip().splitlines()[-window:]
    return [json.loads(x) for x in lines if x.strip()]


def check_drift(cfg: dict, reference: dict | None) -> dict:
    d = cfg["drift"]
    recent = read_recent(cfg["paths"]["query_log"], d["window"])
    out = {"n_samples": len(recent), "drift_detected": False, "reasons": [], "decision": "ok"}
    if not reference or len(recent) < d["min_samples"]:
        out["note"] = "not enough data yet"
        return out
    cur = {
        "mean_top_score": float(np.mean([r["top_score"] for r in recent])),
        "refusal_rate": float(np.mean([not r["answered"] for r in recent])),
        "mean_query_len": float(np.mean([r["query_len"] for r in recent])),
    }
    out["current"], out["reference"] = cur, reference
    if cur["mean_top_score"] < reference["mean_top_score"] * (1 - d["score_drop"]):
        out["reasons"].append("retrieval scores dropped")
    if cur["refusal_rate"] > reference["refusal_rate"] + d["refusal_increase"]:
        out["reasons"].append("more unanswered questions")
    out["drift_detected"] = bool(out["reasons"])
    # Alert / retraining decision (the loop in the workflow diagram)
    out["decision"] = "alert_hr_and_retrain" if out["drift_detected"] else "ok"
    return out


if __name__ == "__main__":  # used by the Airflow drift DAG: exit code 1 = drift
    import sys

    from ragops.config import load_config
    cfg = load_config()
    meta = read_json(cfg["paths"]["index_dir"] / "meta.json", {})
    res = check_drift(cfg, meta.get("reference"))
    print(res)
    sys.exit(1 if res["drift_detected"] else 0)
