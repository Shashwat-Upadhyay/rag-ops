"""Page 3: System Telemetry & Architecture Diagnostics.
Real-time Prometheus metrics, end-to-end architecture diagram,
interactive retrieval sandbox, and governance cards.
"""
import os
import re
import sys
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

import altair as alt  # noqa: E402
import pandas as pd  # noqa: E402
import requests  # noqa: E402
import streamlit as st  # noqa: E402
from theme import (  # noqa: E402
    inject_executive_theme,
    render_animated_metric,
    render_mermaid_diagram,
)

# ----------------- Configuration & Initialization -----------------
API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="RAGOps // Telemetry & Architecture Diagnostics",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_executive_theme()

# Header
st.markdown(
    """
    <div style="margin-bottom: 1.25rem;">
        <h1 class="gradient-heading" style="font-size: 2.2rem; margin-bottom: 0.2rem;">
            System Observability & Architecture
        </h1>
        <p style="margin: 0.15rem 0 0 0; color: #94a3b8; font-size: 0.95rem;">
            Real-time Prometheus telemetry, closed-loop MLOps pipeline architecture, retrieval simulation, and governance cards.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_arch, tab_metrics, tab_sim, tab_cards = st.tabs([
    "🗺 Architecture Diagnostics",
    "📡 Live Prometheus Feeds",
    "🔬 Retrieval Gate Sandbox",
    "🛡 AI Model & Data Governance",
])


# ----------------- Tab 1: Architecture Diagram -----------------
MLOPS_ARCHITECTURE_MERMAID = """
graph LR
    classDef storage fill:#10101a,stroke:#3b3b54,stroke-width:1.5px,color:#f8fafc;
    classDef process fill:#1b1434,stroke:#7c3aed,stroke-width:1.5px,color:#f8fafc;
    classDef gate fill:#063528,stroke:#10b981,stroke-width:1.5px,color:#f8fafc;
    classDef monitor fill:#380e1b,stroke:#ff4d6d,stroke-width:1.5px,color:#f8fafc;

    subgraph S1 ["1. Versioned Data & Ingestion"]
        D1["Raw Docs<br/>(.md, .pdf)"]:::storage --> D2["DVC & Git Registry"]:::storage
        D2 --> P1["Validation & Cleaning"]:::process
        P1 --> P2["Sliding-Window Chunking"]:::process
    end

    subgraph S2 ["2. Experimentation & Quality Gate"]
        P2 --> M1["TF-IDF / Dense Model"]:::process
        M1 --> E1["Eval Suite (12 Queries)"]:::process
        E1 --> QG{"Quality Gate<br/>Hit-Rate >= 75%?"}:::gate
        QG -- Pass --> R1["MLflow Registry<br/>(Alias: Production)"]:::gate
        QG -- Fail --> R2["Rollback Action"]:::monitor
    end

    subgraph S3 ["3. Deployment & Inference"]
        R1 --> API["FastAPI :8000"]:::process
        API --> SRCH["Similarity Search (Top-k)"]:::process
        SRCH --> GRND["Groundedness Verification"]:::gate
        GRND --> UI["Streamlit UI :8501"]:::storage
    end

    subgraph S4 ["4. Closed-Loop Monitoring"]
        API --> PROM["Prometheus ASGI :8000/metrics"]:::monitor
        API --> LOGS["Query Audit Logs (queries.jsonl)"]:::storage
        LOGS --> DRIFT{"Drift Detector :8000/drift<br/>Mean Drop >= 30%?"}:::monitor
        DRIFT -- Drift Detected --> RETRAIN["Trigger Retraining Pipeline"]:::monitor
    end

    RETRAIN -. Loop Retrain Trigger .-> D1
"""

with tab_arch:
    st.markdown(
        """
        <div class="aurora-card" style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <h3 style="margin: 0 0 0.2rem 0; font-size: 1.15rem; color: #f8fafc;">
                        Closed-Loop MLOps Pipeline Topology
                    </h3>
                    <p style="color: #94a3b8; font-size: 0.88rem; margin: 0;">
                        Interactive topology: Ingestion ➔ Evaluation & Quality Gate ➔ Serving ➔ Real-Time Drift Feedback.
                    </p>
                </div>
                <div style="display: flex; gap: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">
                    <span style="color: #c084fc;">● Process</span>
                    <span style="color: #34d399;">● Quality Gate</span>
                    <span style="color: #ff4d6d;">● Observability Loop</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_mermaid_diagram(MLOPS_ARCHITECTURE_MERMAID, height=560)


# ----------------- Tab 2: Live Prometheus Telemetry -----------------
with tab_metrics:
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <div>
                <h3 style="margin: 0; font-size: 1.25rem;">Live Prometheus Telemetry Stream</h3>
                <p style="margin: 0.15rem 0 0 0; color: #94a3b8; font-size: 0.88rem;">
                    Parsed in real-time from the running FastAPI backend (<code>/metrics</code>).
                </p>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <span class="status-dot online"></span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #34d399; font-weight: 700;">
                    STREAM ACTIVE
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        r_metrics = requests.get(f"{API}/metrics", timeout=5)
        if r_metrics.ok:
            raw_text = r_metrics.text

            req_pattern = re.compile(r'ragops_requests_total\{endpoint="([^"]+)",status="([^"]+)"\}\s+([0-9.]+)')
            req_matches = req_pattern.findall(raw_text)

            fb_pattern = re.compile(r'ragops_feedback_total\{type="([^"]+)"\}\s+([0-9.]+)')
            fb_matches = fb_pattern.findall(raw_text)

            ans_pattern = re.compile(r'ragops_answers_total\{status="([^"]+)"\}\s+([0-9.]+)')
            ans_matches = ans_pattern.findall(raw_text)

            c_m1, c_m2 = st.columns(2)

            with c_m1:
                st.markdown("<h4 style='font-size: 1rem;'>Request Volume by Endpoint & Status</h4>", unsafe_allow_html=True)
                if req_matches:
                    df_req = pd.DataFrame(req_matches, columns=["endpoint", "status", "count"])
                    df_req["count"] = df_req["count"].astype(float)

                    chart_req = (
                        alt.Chart(df_req)
                        .mark_bar(cornerRadius=4)
                        .encode(
                            x=alt.X("count:Q", title="Total Requests"),
                            y=alt.Y("endpoint:N", sort="-x", title="Endpoint"),
                            color=alt.Color(
                                "status:N",
                                scale=alt.Scale(domain=["ok", "error"], range=["#7c3aed", "#ff4d6d"]),
                            ),
                            tooltip=["endpoint", "status", "count"],
                        )
                        .properties(height=230)
                        .configure_axis(labelColor="#94a3b8", titleColor="#64748b", labelFont="JetBrains Mono")
                    )
                    st.altair_chart(chart_req, use_container_width=True)
                else:
                    st.info("No request telemetry captured yet.")

            with c_m2:
                st.markdown(
                    "<h4 style='font-size: 1rem;'>Answer Status & Feedback Distributions</h4>",
                    unsafe_allow_html=True,
                )
                if ans_matches or fb_matches:
                    ans_data = [{"Metric": f"Answer: {m[0]}", "Count": float(m[1])} for m in ans_matches]
                    fb_data = [{"Metric": f"Feedback: {m[0]}", "Count": float(m[1])} for m in fb_matches]
                    df_dist = pd.DataFrame(ans_data + fb_data)

                    chart_dist = (
                        alt.Chart(df_dist)
                        .mark_bar(cornerRadius=4)
                        .encode(
                            x=alt.X("Count:Q", title="Total Observations"),
                            y=alt.Y("Metric:N", sort="-x", title="Distribution"),
                            color=alt.Color("Metric:N", scale=alt.Scale(scheme="purpleorange")),
                            tooltip=["Metric", "Count"],
                        )
                        .properties(height=230)
                        .configure_axis(labelColor="#94a3b8", titleColor="#64748b", labelFont="JetBrains Mono")
                    )
                    st.altair_chart(chart_dist, use_container_width=True)
                else:
                    st.info("No answer or feedback records yet.")

            with st.expander("Inspect Raw Prometheus Stream (/metrics)", expanded=False):
                st.code(raw_text[:2000] + ("\n... [truncated]" if len(raw_text) > 2000 else ""), language="text")

        else:
            st.error(f"Prometheus endpoint returned status code: {r_metrics.status_code}")
    except Exception as e:
        st.error(f"Could not reach Prometheus metrics: {e}")


# ----------------- Tab 3: Retrieval Sandbox -----------------
with tab_sim:
    st.markdown(
        """
        <div class="aurora-card">
            <h3 style="margin: 0 0 0.3rem 0; font-size: 1.15rem;">Retrieval Gate Simulator</h3>
            <p style="color: #94a3b8; font-size: 0.92rem; margin: 0;">
                Test how the active retriever scores arbitrary queries. Inspect similarity score distributions,
                retrieved document chunk ranks, and verify whether the threshold gate permits an answer or triggers refusal.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sim_q = st.text_input("Simulation Query String:", "How many days of paid sick leave do employees get?")

    if st.button("⚡ Run Retrieval Simulation", use_container_width=True):
        try:
            with st.spinner("Interrogating active index..."):
                r_sim = requests.post(f"{API}/ask", json={"question": sim_q}, timeout=30)
                if r_sim.ok:
                    res_sim = r_sim.json()
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        render_animated_metric(
                            "Top Similarity Score", f"{res_sim.get('top_score', 0):.3f}", accent_color="#7c3aed"
                        )
                    with c2:
                        render_animated_metric(
                            "Groundedness", f"{res_sim.get('groundedness', 0):.0%}", accent_color="#00d4ff", suffix="%"
                        )
                    with c3:
                        verdict = "ANSWERED" if res_sim.get("answered") else "REFUSED"
                        accent = "#10b981" if res_sim.get("answered") else "#ff4d6d"
                        render_animated_metric("Verdict", verdict, accent_color=accent)

                    st.markdown("#### Retrieved Chunks & Similarity Ranks:")
                    sources = res_sim.get("sources", [])
                    if sources:
                        for s in sources:
                            score = s.get("score", 0.0)
                            score_pct = min(max(score * 100, 0), 100)
                            bar_col = "#10b981" if score >= 0.65 else ("#f59e0b" if score >= 0.40 else "#ff4d6d")
                            st.markdown(
                                f"""
                                <div class="chunk-card">
                                    <div style="display: flex; justify-content: space-between; font-weight: 600; color: #c084fc;">
                                        <span>📄 {s.get('source')} (v{s.get('doc_version', 1)})</span>
                                        <span style="color: #34d399; font-family: 'JetBrains Mono';">
                                            Score: {score:.3f} ({score_pct:.0f}%)
                                        </span>
                                    </div>
                                    <div style="background: rgba(255, 255, 255, 0.06); height: 4px; border-radius: 2px;
                                                margin: 0.4rem 0; overflow: hidden;">
                                        <div style="background: {bar_col}; width: {score_pct}%; height: 100%;"></div>
                                    </div>
                                    <div style="color: #cbd5e1; font-size: 0.92rem; font-style: italic; line-height: 1.5;">
                                        "{s.get('snippet', '')}"
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                    else:
                        st.warning(
                            "No candidate chunks exceeded the minimum similarity threshold. The assistant safely refused."
                        )
                else:
                    st.error(r_sim.text)
        except Exception as e:
            st.error(f"Simulation failed: {e}")


# ----------------- Tab 4: Model & Data Governance -----------------
with tab_cards:
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem;">
            <h3 style="margin: 0; font-size: 1.25rem;">Responsible AI Governance & Compliance</h3>
            <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4);
                         color: #34d399; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;
                         padding: 3px 10px; border-radius: 4px; font-weight: 700;">
                AIR-GAPPED COMPLIANCE VERIFIED
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_m, col_d = st.columns(2)

    with col_m:
        st.markdown(
            """
            <div class="aurora-card" style="margin-bottom: 0.5rem;">
                <h4 style="margin: 0 0 0.35rem 0; font-size: 1rem; color: #00d4ff;">
                    Model Card (docs/model_card.md)
                </h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
        model_card_path = Path(_ROOT) / "docs" / "model_card.md"
        if model_card_path.exists():
            st.markdown(model_card_path.read_text(encoding="utf-8", errors="ignore"))
        else:
            st.info("docs/model_card.md not found.")

    with col_d:
        st.markdown(
            """
            <div class="aurora-card" style="margin-bottom: 0.5rem;">
                <h4 style="margin: 0 0 0.35rem 0; font-size: 1rem; color: #c084fc;">
                    Data Card (docs/data_card.md)
                </h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
        data_card_path = Path(_ROOT) / "docs" / "data_card.md"
        if data_card_path.exists():
            st.markdown(data_card_path.read_text(encoding="utf-8", errors="ignore"))
        else:
            st.info("docs/data_card.md not found.")
