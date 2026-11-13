"""FastAPI backend: employee Q&A + HR document management + health + Prometheus metrics."""
import os
import time
from pathlib import Path

from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
from pydantic import BaseModel, Field

from monitoring import metrics as M
from monitoring.drift import check_drift
from ragops import pipeline
from ragops.documents import SUPPORTED
from ragops.explain import explain_query
from ragops.service import RagService
from ragops.utils import read_json

app = FastAPI(title="RAGOps Knowledge Assistant", version="0.1.0")
app.mount("/metrics", make_asgi_app())
svc = RagService()
HR_TOKEN = os.getenv("HR_TOKEN", "hr-demo")


class Question(BaseModel):
    question: str = Field(min_length=3, max_length=500)


class Feedback(BaseModel):
    helpful: bool


def _track(endpoint: str, start: float, status: str):
    M.REQUESTS.labels(endpoint, status).inc()
    M.LATENCY.labels(endpoint).observe(time.perf_counter() - start)


def _require_hr(token: str | None):
    if token != HR_TOKEN:
        raise HTTPException(401, "Invalid HR token")


def _require_index():
    if not svc.ready:
        raise HTTPException(503, "No index yet. HR must upload documents (or run `make pipeline`).")


@app.get("/health")
def health():
    meta = svc.index.meta if svc.ready else {}
    return {"status": "ok" if svc.ready else "no_index", "index_loaded": svc.ready,
            "index_version": meta.get("index_version"), "retriever": svc.index.exp["retriever"] if svc.ready else None,
            "documents": meta.get("docs", {})}


@app.post("/ask")
def ask(q: Question):
    t0 = time.perf_counter()
    try:
        _require_index()
        res = svc.ask(q.question)
    except HTTPException:
        _track("ask", t0, "error")
        raise
    except Exception as e:  # unexpected failure -> clean 500 + counted as error
        _track("ask", t0, "error")
        return JSONResponse(status_code=500, content={"detail": f"Internal error: {e}"})
    M.ANSWERS.labels("answered" if res["answered"] else "no_answer").inc()
    M.TOP_SCORE.observe(min(res["top_score"], 1.0))
    if res["answered"]:
        M.GROUNDEDNESS.observe(res["groundedness"])
    _track("ask", t0, "ok")
    return res


@app.post("/explain")
def explain(q: Question):
    _require_index()
    return {"question": q.question, "terms": explain_query(svc.index, q.question)}


@app.post("/feedback")
def feedback(f: Feedback):
    M.FEEDBACK.labels("up" if f.helpful else "down").inc()
    return {"ok": True}


@app.get("/drift")
def drift():
    meta = svc.index.meta if svc.ready else {}
    res = check_drift(svc.cfg, meta.get("reference"))
    M.DRIFT.set(1 if res["drift_detected"] else 0)
    return res


# ---------------- HR endpoints ----------------
def _rebuild() -> dict:
    with svc.lock:
        try:
            promoted = pipeline.run_all(svc.cfg)
        except ValueError as e:   # validation failed
            raise HTTPException(422, str(e))
        svc.reload()
        if svc.ready:
            M.INDEX_DOCS.set(len(svc.index.meta.get("docs", {})))
    return {"promoted": promoted, "metrics": read_json(svc.cfg["paths"]["metrics_file"], {})}


@app.get("/admin/documents")
def list_documents(x_hr_token: str | None = Header(default=None)):
    _require_hr(x_hr_token)
    return read_json(svc.cfg["paths"]["registry"], {})


@app.post("/admin/upload")
def upload(files: list[UploadFile] = File(...), x_hr_token: str | None = Header(default=None)):
    _require_hr(x_hr_token)
    raw = svc.cfg["paths"]["raw_dir"]
    raw.mkdir(parents=True, exist_ok=True)
    saved = []
    for f in files:
        name = Path(f.filename).name                      # strip any path
        if Path(name).suffix.lower() not in SUPPORTED:
            raise HTTPException(400, f"{name}: only {', '.join(sorted(SUPPORTED))} files are supported")
        (raw / name).write_bytes(f.file.read())
        saved.append(name)
    return {"saved": saved, **_rebuild()}


@app.delete("/admin/documents/{name}")
def delete_document(name: str, x_hr_token: str | None = Header(default=None)):
    _require_hr(x_hr_token)
    path = svc.cfg["paths"]["raw_dir"] / Path(name).name
    if not path.exists():
        raise HTTPException(404, "Document not found")
    path.unlink()
    return {"deleted": name, **_rebuild()}
