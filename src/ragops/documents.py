"""Load documents, clean text, chunk, and keep a simple version registry."""
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path

from .utils import read_json, write_json

SUPPORTED = {".md", ".txt", ".pdf"}


def read_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        return "\n".join((p.extract_text() or "") for p in PdfReader(str(path)).pages)
    return path.read_text(encoding="utf-8", errors="ignore")


def load_documents(raw_dir: Path) -> list[dict]:
    docs = []
    for p in sorted(Path(raw_dir).glob("*")):
        if p.suffix.lower() in SUPPORTED:
            text = read_file(p)
            docs.append({"source": p.name, "text": text,
                         "sha256": hashlib.sha256(text.encode()).hexdigest()})
    return docs


def clean_text(text: str) -> str:
    text = re.sub(r"[\x00-\x08\x0b-\x1f]", " ", text)   # control chars
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split into windows of `chunk_size` words with `overlap` words shared."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    words = text.split()
    step = chunk_size - overlap
    chunks = []
    for start in range(0, max(len(words), 1), step):
        piece = words[start:start + chunk_size]
        if piece:
            chunks.append(" ".join(piece))
        if start + chunk_size >= len(words):
            break
    return chunks


def make_chunks(docs: list[dict], chunk_size: int, overlap: int) -> list[dict]:
    out = []
    for d in docs:
        for i, c in enumerate(chunk_text(d["text"], chunk_size, overlap)):
            out.append({"id": f"{d['source']}#{i}", "source": d["source"],
                        "doc_version": d.get("version", 1), "text": c})
    return out


def update_registry(docs: list[dict], registry_path: Path) -> dict:
    """Document versioning: version +1 whenever a file's content hash changes."""
    reg = read_json(registry_path, {})
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    current = {d["source"] for d in docs}
    for d in docs:
        old = reg.get(d["source"])
        if old is None:
            reg[d["source"]] = {"version": 1, "sha256": d["sha256"], "updated_at": now}
        elif old["sha256"] != d["sha256"]:
            reg[d["source"]] = {"version": old["version"] + 1, "sha256": d["sha256"], "updated_at": now}
        d["version"] = reg[d["source"]]["version"]
    reg = {k: v for k, v in reg.items() if k in current}  # drop deleted files
    write_json(registry_path, reg)
    return reg


def docs_fingerprint(registry: dict) -> str:
    """Short id of the exact set of document versions an index was built from."""
    raw = "|".join(f"{k}:{v['sha256']}" for k, v in sorted(registry.items()))
    return hashlib.sha256(raw.encode()).hexdigest()[:10]
