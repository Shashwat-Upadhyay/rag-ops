"""An Index = chunks + a fitted retriever + metadata. Saved as a folder."""
from pathlib import Path

import numpy as np

from .retrievers import RETRIEVERS
from .utils import read_json, write_json


class Index:
    def __init__(self, exp: dict, chunks: list[dict], retriever, meta: dict | None = None, cfg: dict | None = None):
        self.exp, self.chunks, self.retriever = exp, chunks, retriever
        self.meta, self.cfg = meta or {}, cfg or {}

    @classmethod
    def build(cls, exp, chunks, cfg):
        r = RETRIEVERS[exp["retriever"]]().fit([c["text"] for c in chunks], cfg)
        return cls(exp, chunks, r, cfg=cfg)

    def search(self, query: str, k: int | None = None) -> list[dict]:
        s = self.retriever.scores(query)
        k = k or self.exp["top_k"]
        top = np.argsort(-s)[:k]
        return [{**self.chunks[i], "score": float(s[i])} for i in top]

    def top_score(self, query: str) -> float:
        return float(self.retriever.scores(query).max())

    def save(self, d: Path):
        d = Path(d)
        d.mkdir(parents=True, exist_ok=True)
        write_json(d / "chunks.json", self.chunks)
        write_json(d / "meta.json", {**self.meta, "exp": self.exp})
        self.retriever.save(d)

    @classmethod
    def load(cls, d: Path, cfg: dict):
        d = Path(d)
        meta = read_json(d / "meta.json")
        if meta is None:
            raise FileNotFoundError(f"No index at {d}. Run `make pipeline` first.")
        exp = meta["exp"]
        r = RETRIEVERS[exp["retriever"]]().load(d, cfg)
        return cls(exp, read_json(d / "chunks.json"), r, meta, cfg)
