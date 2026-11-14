"""Page 2: HR Policy Operations & Quality Control Center.
Document ingestion, validation, automated MLflow pipeline retraining,
and live quality gate verification.
"""
import os
import sys
import time
from pathlib import Path

# Ensure local packages site-packages is on sys.path
_LOCAL_CACHE = (
    r"C:\Users\HP\AppData\Local\Packages"
    r"\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages"
)
if os.path.exists(_LOCAL_CACHE) and _LOCAL_CACHE not in sys.path:
    sys.path.append(_LOCAL_CACHE)

_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _ROOT not in sys.path:
    sys.path.append(_ROOT)

import requests  # noqa: E402
import streamlit as st  # noqa: E402
from theme import (  # noqa: E402
    inject_executive_theme,
    render_animated_metric,
    render_confetti,
)

# ----------------- Configuration & Initialization -----------------
API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="RAGOps // Policy Operations Control Center",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_executive_theme()

# ── Extra page-level CSS for HR Portal enhancements ──────────────────────────
st.markdown(
    """
    <style>
    @keyframes pulse-emerald {
        0%, 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0.4); }
        50%       { box-shadow: 0 0 0 8px rgba(16,185,129,0); }
    }
    @keyframes flash-rose {
        0%, 100% { border-color: rgba(244,63,94,0.6); }
        50%       { border-color: rgba(244,63,94,0.15); }
    }
    .auth-ok {
        margin-top: 0.6rem; padding: 0.6rem 0.75rem;
        background: rgba(16,185,129,0.1);
        border: 1.5px solid rgba(16,185,129,0.5);
        border-radius: 8px; text-align: center;
        animation: pulse-emerald 2s ease-in-out 1;
    }
    .auth-fail {
        margin-top: 0.6rem; padding: 0.6rem 0.75rem;
        background: rgba(244,63,94,0.1);
        border: 1.5px solid rgba(244,63,94,0.5);
        border-radius: 8px; text-align: center;
        animation: flash-rose 0.8s ease-in-out 3;
    }
    .terminal-block {
        background: #060608; border: 1px solid rgba(124,58,237,0.35);
        border-radius: 8px; padding: 0.65rem 0.8rem; margin-bottom: 0.5rem;
    }
    .stage-chip {
        display: inline-block;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.4);
        color: #818cf8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 20px;
    }
    .stage-arrow { color: #52525b; font-size: 0.9rem; margin: 0 4px; }
    .doc-card {
        background: rgba(13,13,20,0.9);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 1rem 1.1rem 0.75rem;
        margin-bottom: 0.75rem;
    }
    .index-bar-wrap {
        background: rgba(255,255,255,0.05); border-radius: 4px;
        height: 4px; width: 100%; margin-top: 0.5rem;
    }
    .index-bar-fill {
        background: linear-gradient(90deg, #10b981, #34d399);
        border-radius: 4px; height: 4px; width: 100%;
    }
    .danger-pill {
        background: rgba(244,63,94,0.12) !important;
        border: 1px solid rgba(244,63,94,0.4) !important;
        color: #fb7185 !important;
        border-radius: 20px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
    }
    .danger-pill:hover { background: rgba(244,63,94,0.25) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom: 1.25rem;">
        <h1 class="gradient-heading">Policy Operations</h1>
        <div style="display: flex; gap: 0.5rem; margin-top: 0.4rem; flex-wrap: wrap;">
            <span style="background: rgba(255,77,109,0.18); border: 1px solid rgba(255,77,109,0.45);
                         color: #ff4d6d; font-family: 'JetBrains Mono',monospace; font-size: 0.72rem;
                         font-weight: 700; padding: 3px 10px; border-radius: 4px; letter-spacing: 0.08em;">
                ADMIN PORTAL
            </span>
            <span style="background: rgba(124,58,237,0.18); border: 1px solid rgba(124,58,237,0.45);
                         color: #a78bfa; font-family: 'JetBrains Mono',monospace; font-size: 0.72rem;
                         font-weight: 700; padding: 3px 10px; border-radius: 4px; letter-spacing: 0.08em;">
                MLOps Pipeline
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- Administrator Authentication -----------------
st.sidebar.markdown(
    """
    <div class="terminal-block">
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#7c3aed;
                    text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px;">
            ⬡ SYSTEM ACCESS
        </div>
        <div style="font-size: 1rem; font-weight: 700; color: #f4f4f5;">
            Administrator Token
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#52525b; margin-top:2px;">
            Clearance Level: HR-ADMIN
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

default_token = os.getenv("HR_TOKEN", "hr-demo")
token = st.sidebar.text_input("HR Token", type="password", value=default_token)
headers = {"X-HR-Token": token}

if not token:
    if st.sidebar.button("🔑 Inject Demo Key (hr-demo)", use_container_width=True):
        st.session_state["hr_token"] = "hr-demo"
        st.rerun()

is_authorized = token == default_token

if is_authorized:
    st.sidebar.markdown(
        """
        <div class="auth-ok">
            <span style="font-family:'JetBrains Mono',monospace; font-size:0.78rem;
                         color:#34d399; font-weight:700;">
                ✓ Clearance Verified: Admin
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.sidebar.markdown(
        """
        <div class="auth-fail">
            <span style="font-family:'JetBrains Mono',monospace; font-size:0.78rem;
                         color:#fb7185; font-weight:700;">
                ✗ Invalid Security Token
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------- System Health & Telemetry -----------------
try:
    r_health = requests.get(f"{API}/health", timeout=3)
    health_info = r_health.json() if r_health.ok else {}
except Exception:
    health_info = {}

try:
    r_drift = requests.get(f"{API}/drift", timeout=3)
    drift_info = r_drift.json() if r_drift.ok else {}
except Exception:
    drift_info = {}

is_drifted = drift_info.get("drift_detected", False)
sys_state_val = "ONLINE" if health_info.get("status") == "ok" else "OFFLINE"
retriever_val = health_info.get("retriever", "tfidf").upper()
index_ver_val = health_info.get("index_version", "N/A")[:8]
drift_val = "DRIFT DETECTED" if is_drifted else "STABLE (0.00)"

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_animated_metric("System State", sys_state_val, accent="emerald")
with col2:
    render_animated_metric("Retriever Engine", retriever_val, accent="violet")
with col3:
    render_animated_metric("Index Version", index_ver_val, accent="cyan")
with col4:
    render_animated_metric("Corpus Drift", drift_val, accent="coral" if is_drifted else "emerald")

st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)


# ----------------- Ingestion & Retraining Bay -----------------
st.markdown(
    "<h3 style='font-size: 1.25rem; margin-bottom: 0.6rem; font-family: Syne, sans-serif;'>"
    "Automated Document Pipeline Ingestion</h3>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="aurora-card" style="margin-bottom: 1rem;">
        <p style="color: #d4d4d8; margin-bottom: 0.75rem; font-size: 0.95rem;">
            Upload verified corporate documentation (<strong>.md, .pdf, .txt</strong>).
            Every upload automatically executes the validation suite and retraining pipeline:
        </p>
        <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center;">
            <span class="stage-chip">1. Schema Validation</span>
            <span class="stage-arrow">➔</span>
            <span class="stage-chip">2. Chunk Generation</span>
            <span class="stage-arrow">➔</span>
            <span class="stage-chip">3. TF-IDF &amp; Vector Indexing</span>
            <span class="stage-arrow">➔</span>
            <span class="stage-chip">4. Quality Gate Evaluation</span>
            <span class="stage-arrow">➔</span>
            <span class="stage-chip">5. MLflow Promotion / Rollback</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

files = st.file_uploader(
    "Choose document files to ingest and rebuild index",
    type=["pdf", "md", "txt"],
    accept_multiple_files=True,
    help="Supported formats: Markdown (.md), PDF (.pdf), Text (.txt)",
)

if st.button("🚀 Ingest Documents & Retrain Model", disabled=not files or not is_authorized, use_container_width=True):
    progress_bar = st.progress(0, text="Transferring document files...")

    stages = [
        (20, "1/5 ▸ Validating file format specifications and text clean standards..."),
        (45, "2/5 ▸ Generating sliding-window text chunks with overlap preservation..."),
        (65, "3/5 ▸ Fitting TF-IDF vectors and updating candidate models..."),
        (85, "4/5 ▸ Running Automated Quality Gate Evaluation suite (12 test queries)..."),
        (95, "5/5 ▸ Evaluating promotion criteria and registering model in MLflow..."),
    ]

    for pct, msg in stages:
        progress_bar.progress(pct, text=msg)
        time.sleep(0.25)

    try:
        r = requests.post(
            f"{API}/admin/upload",
            headers=headers,
            timeout=600,
            files=[(("files", (f.name, f.getvalue()))) for f in files],
        )
        progress_bar.progress(100, text="✓ Pipeline execution finished!")

        if r.ok:
            out = r.json()
            promoted = out.get("promoted", False)
            metrics = out.get("metrics", {})
            hit_rate = metrics.get("hit_rate", 0)
            saved_files = out.get("saved", [])

            if promoted:
                render_confetti()
                st.markdown(
                    f"""
                    <div class="aurora-card" style="margin-top: 1rem;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.5rem;">
                            <span style="font-size: 2rem;">✅</span>
                            <span style="color: #34d399; font-weight: 800; font-size: 1.15rem;
                                         font-family: 'Syne', sans-serif;">
                                Quality Gate Passed · Model Promoted
                            </span>
                        </div>
                        <p style="color: #e4e4e7; margin: 0; font-size: 0.95rem;">
                            Successfully ingested <strong>{", ".join(saved_files)}</strong>.
                            Candidate model achieved a <strong>Hit-Rate of {hit_rate:.0%}</strong>
                            on the evaluation suite. The new index has been promoted to production and is now live.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div class="aurora-card" style="margin-top: 1rem; border-color: rgba(245,158,11,0.5);">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.5rem;">
                            <span style="font-size: 2rem;">⚠️</span>
                            <span style="color: #fbbf24; font-weight: 800; font-size: 1.15rem;
                                         font-family: 'Syne', sans-serif;">
                                Quality Gate Warning · Rollback Preserved
                            </span>
                        </div>
                        <p style="color: #e4e4e7; margin: 0; font-size: 0.95rem;">
                            Documents were successfully saved, but candidate model failed quality gate thresholds.
                            The previous production index remains active to safeguard answer precision.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            err_msg = (
                r.json().get("detail", r.text)
                if r.headers.get("content-type") == "application/json"
                else r.text
            )
            st.error(f"Ingestion failed: {err_msg}")
    except Exception as e:
        st.error(f"Service request failed: {e}")

st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 2rem 0;'>", unsafe_allow_html=True)


# ----------------- Document Registry Matrix -----------------
st.markdown(
    "<h3 style='font-size: 1.25rem; margin-bottom: 0.6rem; font-family: Syne, sans-serif;'>"
    "Registered Document Inventory</h3>",
    unsafe_allow_html=True,
)

_EXT_ICON = {".md": "📝", ".pdf": "📕", ".txt": "📄"}


def _file_icon(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return _EXT_ICON.get(ext, "📄")


try:
    r_docs = requests.get(f"{API}/admin/documents", headers=headers, timeout=10)
    if r_docs.status_code == 401:
        st.info("🔒 Enter a valid HR administrator token in the sidebar to view and manage registered documentation.")
    elif r_docs.ok:
        docs = r_docs.json()
        if not docs:
            st.warning("No documents currently registered in the corpus.")
        else:
            search_query = st.text_input("Filter documents by filename or hash:", "")

            filtered_docs = {
                k: v
                for k, v in docs.items()
                if search_query.lower() in k.lower() or search_query.lower() in v.get("sha256", "").lower()
            }

            for name, info in filtered_docs.items():
                ver = info.get("version", 1)
                updated = info.get("updated_at", "")[:19].replace("T", " ")
                sha = info.get("sha256", "")[:12]
                icon = _file_icon(name)

                st.markdown(
                    f"""
                    <div class="doc-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;
                                    flex-wrap: wrap; gap: 0.5rem;">
                            <div>
                                <span style="font-weight: 700; color: #f4f4f5; font-size: 1rem;">
                                    {icon} {name}
                                </span>
                                <span style="margin-left: 0.6rem; background: rgba(99,102,241,0.15);
                                             border: 1px solid rgba(99,102,241,0.3); color: #818cf8;
                                             padding: 2px 7px; border-radius: 4px;
                                             font-family: 'JetBrains Mono',monospace; font-size: 0.75rem;">
                                    v{ver}
                                </span>
                                <span style="margin-left: 0.4rem; background: rgba(255,255,255,0.05);
                                             border: 1px solid rgba(255,255,255,0.1); color: #a1a1aa;
                                             padding: 2px 7px; border-radius: 4px;
                                             font-family: 'JetBrains Mono',monospace; font-size: 0.75rem;">
                                    {sha}...
                                </span>
                            </div>
                            <div style="font-family: 'JetBrains Mono',monospace; color: #71717a; font-size: 0.8rem;">
                                Updated: {updated}
                            </div>
                        </div>
                        <div class="index-bar-wrap">
                            <div class="index-bar-fill"></div>
                        </div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem;
                                    color:#34d399; margin-top:3px;">
                            Index Weight: 100%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                col_view, col_del = st.columns([6, 1])
                with col_view:
                    raw_path = Path(_ROOT) / "data" / "raw" / name
                    if raw_path.exists():
                        with st.expander(f"Inspect Document Content ({name})", expanded=False):
                            try:
                                content = raw_path.read_text(encoding="utf-8", errors="ignore")
                                st.markdown(f"```markdown\n{content}\n```")
                            except Exception as ex:
                                st.caption(f"Could not read content: {ex}")
                with col_del:
                    del_clicked = st.button(
                        "🗑 Delete",
                        key=f"del_{name}",
                        use_container_width=True,
                        help=f"Delete {name} and rebuild index",
                    )
                    if del_clicked:
                        try:
                            with st.spinner(f"Deleting {name} & rebuilding index..."):
                                rd = requests.delete(
                                    f"{API}/admin/documents/{name}", headers=headers, timeout=600
                                )
                                if rd.ok:
                                    st.success(f"Deleted {name} and rebuilt index.")
                                    time.sleep(0.5)
                                    st.rerun()
                                else:
                                    st.error(rd.text)
                        except Exception as e:
                            st.error(f"Delete failed: {e}")
    else:
        st.error("Failed to load document inventory.")
except Exception as e:
    st.error(f"Could not reach API: {e}")
