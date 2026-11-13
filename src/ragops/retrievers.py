"""Three simple retrievers: TF-IDF (baseline), dense embeddings, and hybrid (both)."""
from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfRetriever:
    name = "tfidf"

    def fit(self, texts, cfg=None):
        self.vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
        self.matrix = self.vec.fit_transform(texts)
        return self

    def scores(self, query: str) -> np.ndarray:
        return (self.matrix @ self.vec.transform([query]).T).toarray().ravel()

    def save(self, d: Path):
        joblib.dump((self.vec, self.matrix), d / "tfidf.joblib")

    def load(self, d: Path, cfg=None):
        self.vec, self.matrix = joblib.load(d / "tfidf.joblib")
        return self


class DenseRetriever:
    name = "dense"
    _model = None

    def _embed(self, texts, cfg):
        from fastembed import TextEmbedding  # imported lazily: optional dependency

        if DenseRetriever._model is None:
            DenseRetriever._model = TextEmbedding(cfg["dense_model"])
        v = np.array(list(DenseRetriever._model.embed(list(texts))), dtype="float32")
        return v / np.linalg.norm(v, axis=1, keepdims=True)

    def fit(self, texts, cfg):
        self.cfg = cfg
        self.emb = self._embed(texts, cfg)
        return self

    def scores(self, query: str) -> np.ndarray:
        return self.emb @ self._embed([query], self.cfg)[0]

    def save(self, d: Path):
        np.save(d / "dense.npy", self.emb)

    def load(self, d: Path, cfg):
        self.cfg = cfg
        self.emb = np.load(d / "dense.npy")
        return self


class HybridRetriever:
    name = "hybrid"

    def fit(self, texts, cfg):
        self.a, self.b = TfidfRetriever().fit(texts), DenseRetriever().fit(texts, cfg)
        return self

    def scores(self, query: str) -> np.ndarray:
        return 0.5 * self.a.scores(query) + 0.5 * self.b.scores(query)

    def save(self, d: Path):
        self.a.save(d)
        self.b.save(d)

    def load(self, d: Path, cfg):
        self.a, self.b = TfidfRetriever().load(d), DenseRetriever().load(d, cfg)
        return self


RETRIEVERS = {"tfidf": TfidfRetriever, "dense": DenseRetriever, "hybrid": HybridRetriever}
