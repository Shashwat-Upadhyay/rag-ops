"""RagService: loads the production index and answers questions."""
import json
import threading
import time
from datetime import datetime, timezone

from .config import load_config, load_prompts
from .generation import NO_ANSWER, generate_answer, groundedness
from .index import Index


class RagService:
    def __init__(self):
        self.cfg = load_config()
        self.index = None
        self.lock = threading.Lock()       # one pipeline run at a time
        self.reload()

    def reload(self):
        try:
            self.index = Index.load(self.cfg["paths"]["index_dir"], self.cfg)
        except FileNotFoundError:
            self.index = None

    @property
    def ready(self) -> bool:
        return self.index is not None

    def ask(self, question: str) -> dict:
        t0 = time.perf_counter()
        prompts = load_prompts()
        results = self.index.search(question)
        top = results[0]["score"]
        answered = top >= self.index.exp["min_score"]
        if answered:
            answer, mode = generate_answer(question, results, prompts["versions"][prompts["active"]], self.cfg)
            ground = groundedness(answer, results)
        else:
            answer, mode, ground = NO_ANSWER, "none", 1.0
        latency = time.perf_counter() - t0
        self._log(question, top, answered, ground, latency)
        return {
            "answer": answer, "answered": answered, "mode": mode,
            "groundedness": ground, "top_score": round(top, 3),
            "sources": [{"source": r["source"], "doc_version": r["doc_version"],
                         "score": round(r["score"], 3), "snippet": r["text"][:300]} for r in results] if answered else [],
            "prompt_version": prompts["active"], "index_version": self.index.meta.get("index_version"),
            "latency_ms": round(latency * 1000, 1),
        }

    def _log(self, question, top, answered, ground, latency):
        path = self.cfg["paths"]["query_log"]
        path.parent.mkdir(parents=True, exist_ok=True)
        row = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "query_len": len(question.split()), "top_score": round(top, 4),
               "answered": answered, "groundedness": ground, "latency_s": round(latency, 4)}
        with open(path, "a") as f:
            f.write(json.dumps(row) + "\n")
