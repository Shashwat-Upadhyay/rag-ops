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
    render_confetti,
)

# ----------------- Configuration & Initialization -----------------
API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="RAGOps // Policy Operations & Quality Control",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_executive_theme()

# Header
st.markdown(
    """
    <div style="margin-bottom: 1.25rem;">
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; letter-spacing: -0.03em;">
            Policy Ingestion & Quality Control Center
        </h1>
        <p style="margin: 0.2rem 0 0 0; color: #a1a1aa; font-size: 0.95rem;">
            Upload, validate, index, and monitor corporate documentation with automated quality gates and rollback protection.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- Administrator Authentication -----------------
st.sidebar.markdown(
    """
    <div style="padding: 0.5rem 0 0.8rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
        <div style="font-size: 0.8rem; font-weight: 700; color: #a1a1aa; text-transform: uppercase; letter-spacing: 0.05em;">
            Access Control
        </div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #f4f4f5; margin-top: 2px;">
            Administrator Token
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
        <div style="margin-top: 0.6rem; padding: 0.45rem 0.65rem; background: rgba(16, 185, 129, 0.1);
                    border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; text-align: center;">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.78rem; color: #34d399; font-weight: 600;">
                ✓ Clearance Verified: Admin
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.sidebar.markdown(
        """
        <div style="margin-top: 0.6rem; padding: 0.45rem 0.65rem; background: rgba(244, 63, 94, 0.1);
                    border: 1px solid rgba(244, 63, 94, 0.3); border-radius: 6px; text-align: center;">
            <span style="font-family: 'JetBrains Mono'; font-size: 0.78rem; color: #fb7185; font-weight: 600;">
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

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("System State", "ONLINE" if health_info.get("status") == "ok" else "OFFLINE")
with col2:
    st.metric("Retriever Engine", health_info.get("retriever", "tfidf").upper())
with col3:
    st.metric("Index Version", health_info.get("index_version", "N/A")[:8])
with col4:
    is_drifted = drift_info.get("drift_detected", False)
    st.metric("Corpus Drift", "DRIFT DETECTED" if is_drifted else "STABLE (0.00)")

st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.06); margin: 1.5rem 0;'>", unsafe_allow_html=True)


# ----------------- Ingestion & Retraining Bay -----------------
st.markdown("<h3 style='font-size: 1.25rem; margin-bottom: 0.4rem;'>Automated Document Pipeline Ingestion</h3>",
            unsafe_allow_html=True)

st.markdown(
    """
    <div class="pro-card">
        <p style="color: #d4d4d8; margin-bottom: 0.5rem; font-size: 0.95rem;">
            Upload verified corporate documentation (<strong>.md, .pdf, .txt</strong>).
            Every upload automatically executes the validation suite and retraining pipeline:
        </p>
        <div style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #818cf8; display: flex; flex-wrap: wrap;
                    gap: 0.5rem; align-items: center;">
            <span>[1. Schema Validation]</span> ➔
            <span>[2. Chunk Generation]</span> ➔
            <span>[3. TF-IDF & Vector Indexing]</span> ➔
            <span>[4. Quality Gate Evaluation]</span> ➔
            <span>[5. MLflow Promotion / Rollback]</span>
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
        (20, "1/5 Validating file format specifications and text clean standards..."),
        (45, "2/5 Generating sliding-window text chunks with overlap preservation..."),
        (65, "3/5 Fitting TF-IDF vectors and updating candidate models..."),
        (85, "4/5 Running Automated Quality Gate Evaluation suite (12 test queries)..."),
        (95, "5/5 Evaluating promotion criteria and registering model in MLflow..."),
    ]

    for pct, msg in stages:
        progress_bar.progress(pct, text=msg)
        time.sleep(0.25)

    try:
        r = requests.post(
            f"{API}/admin/upload",
            headers=headers,
            timeout=600,
            files=[("files", (f.name, f.getvalue())) for f in files],
        )
        progress_bar.progress(100, text="Pipeline execution finished!")

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
                    <div style="margin-top: 1rem; padding: 1.25rem; background: rgba(16, 185, 129, 0.12);
                                border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.35rem;">
                            <span style="color: #34d399; font-weight: 700; font-size: 1.1rem;">
                                ✓ Quality Gate Passed · Model Promoted
                            </span>
                        </div>
                        <p style="color: #e4e4e7; margin: 0; font-size: 0.95rem;">
                            Successfully ingested <strong>{', '.join(saved_files)}</strong>.
                            Candidate model achieved a <strong>Hit-Rate of {hit_rate:.0%}</strong> on the evaluation suite.
                            The new index has been promoted to production and is now live.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div style="margin-top: 1rem; padding: 1.25rem; background: rgba(245, 158, 11, 0.12);
                                border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.35rem;">
                            <span style="color: #fbbf24; font-weight: 700; font-size: 1.1rem;">
                                ⚠ Quality Gate Warning · Rollback Preserved
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
            err_msg = r.json().get("detail", r.text) if r.headers.get("content-type") == "application/json" else r.text
            st.error(f"Ingestion failed: {err_msg}")
    except Exception as e:
        st.error(f"Service request failed: {e}")

st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.06); margin: 2rem 0;'>", unsafe_allow_html=True)


# ----------------- Document Registry Matrix -----------------
st.markdown("<h3 style='font-size: 1.25rem; margin-bottom: 0.4rem;'>Registered Document Inventory</h3>",
            unsafe_allow_html=True)

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
                k: v for k, v in docs.items()
                if search_query.lower() in k.lower() or search_query.lower() in v.get("sha256", "").lower()
            }

            for name, info in filtered_docs.items():
                ver = info.get("version", 1)
                updated = info.get("updated_at", "")[:19].replace("T", " ")
                sha = info.get("sha256", "")[:12]

                st.markdown(
                    f"""
                    <div class="pro-card" style="margin-bottom: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;
                                    flex-wrap: wrap; gap: 0.5rem;">
                            <div>
                                <span style="font-weight: 700; color: #f4f4f5; font-size: 1rem;">
                                    📄 {name}
                                </span>
                                <span style="margin-left: 0.6rem; background: rgba(99, 102, 241, 0.15);
                                             border: 1px solid rgba(99, 102, 241, 0.3); color: #818cf8;
                                             padding: 2px 7px; border-radius: 4px; font-family: 'JetBrains Mono';
                                             font-size: 0.75rem;">
                                    v{ver}
                                </span>
                                <span style="margin-left: 0.4rem; background: rgba(255, 255, 255, 0.05);
                                             border: 1px solid rgba(255, 255, 255, 0.1); color: #a1a1aa;
                                             padding: 2px 7px; border-radius: 4px; font-family: 'JetBrains Mono';
                                             font-size: 0.75rem;">
                                    {sha}...
                                </span>
                            </div>
                            <div style="font-family: 'JetBrains Mono'; color: #71717a; font-size: 0.8rem;">
                                Updated: {updated}
                            </div>
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
                    if st.button("Delete", key=f"del_{name}", use_container_width=True):
                        try:
                            with st.spinner(f"Deleting {name} & rebuilding index..."):
                                rd = requests.delete(f"{API}/admin/documents/{name}", headers=headers, timeout=600)
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
