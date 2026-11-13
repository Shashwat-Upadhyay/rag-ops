"""Offline evaluation of a retriever on data/eval/eval_set.json."""
import time

import numpy as np


def evaluate_index(index, eval_set: list[dict]) -> tuple[dict, list[dict]]:
    min_score = index.exp["min_score"]
    k = index.exp["top_k"]
    rows, hits, rr, recall, decisions, lat = [], [], [], [], [], []
    top_scores, qlens = [], []
    for item in eval_set:
        t0 = time.perf_counter()
        res = index.search(item["question"])
        lat.append((time.perf_counter() - t0) * 1000)
        top = res[0]["score"]
        top_scores.append(top)
        qlens.append(len(item["question"].split()))
        answered = top >= min_score
        exp_src = item["expected_source"]
        row = {"question": item["question"], "top_score": round(top, 3), "answered": answered}
        if exp_src:  # in-scope question
            srcs = [r["source"] for r in res[:k]]
            hit = exp_src in srcs
            hits.append(hit)
            rr.append(1 / (srcs.index(exp_src) + 1) if hit else 0.0)
            ctx = " ".join(r["text"] for r in res).lower()
            kws = item.get("keywords", [])
            recall.append(sum(w.lower() in ctx for w in kws) / len(kws) if kws else 1.0)
            decisions.append(answered)          # should answer
            row.update(hit=hit)
        else:                                    # out-of-scope: should refuse
            decisions.append(not answered)
        rows.append(row)
    metrics = {
        "hit_rate": float(np.mean(hits)),
        "mrr": float(np.mean(rr)),
        "context_recall": float(np.mean(recall)),
        "decision_accuracy": float(np.mean(decisions)),   # answers in-scope, refuses out-of-scope
        "avg_latency_ms": float(np.mean(lat)),
    }
    metrics["selection_score"] = (0.4 * metrics["hit_rate"] + 0.2 * metrics["mrr"]
                                  + 0.2 * metrics["context_recall"] + 0.2 * metrics["decision_accuracy"])
    reference = {  # baseline statistics for drift detection later
        "mean_top_score": float(np.mean(top_scores)),
        "refusal_rate": float(np.mean([not r["answered"] for r in rows])),
        "mean_query_len": float(np.mean(qlens)),
    }
    return metrics, rows, reference
