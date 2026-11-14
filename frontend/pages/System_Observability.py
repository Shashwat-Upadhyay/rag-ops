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
    render_mermaid_diagram,
)

# ----------------- Configuration & Initialization -----------------
API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="RAGOps // Telemetry & Architecture Diagnostics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_executive_theme()

# Header
st.markdown(
    """
    <div style="margin-bottom: 1.25rem;">
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; letter-spacing: -0.03em;">
            System Telemetry & Architecture Diagnostics
        </h1>
        <p style="margin: 0.2rem 0 0 0; color: #a1a1aa; font-size: 0.95rem;">
            Real-time Prometheus telemetry, closed-loop MLOps pipeline architecture, retrieval simulation, and governance cards.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_arch, tab_metrics, tab_sim, tab_cards = st.tabs([
    "Pipeline Architecture",
    "Prometheus Telemetry",
    "Retrieval Sandbox",
    "Model & Data Governance",
])


# ----------------- Tab 1: Architecture Diagram -----------------
MLOPS_ARCHITECTURE_MERMAID = """
graph LR
    classDef storage fill:#18181b,stroke:#52525b,stroke-width:1.5px,color:#f4f4f5;
    classDef process fill:#1e1b4b,stroke:#6366f1,stroke-width:1.5px,color:#f4f4f5;
    classDef gate fill:#064e3b,stroke:#10b981,stroke-width:1.5px,color:#f4f4f5;
    classDef monitor fill:#4c0519,stroke:#f43f5e,stroke-width:1.5px,color:#f4f4f5;

    subgraph S1 ["1. Data & Ingestion"]
        D1["Raw Docs<br/>(.md, .pdf)"]:::storage --> D2["DVC & Git Registry"]:::storage
        D2 --> P1["Validation & Cleaning"]:::process
        P1 --> P2["Chunking Engine"]:::process
    end

    subgraph S2 ["2. Experimentation & Quality Gate"]
        P2 --> M1["TF-IDF / Dense Model"]:::process
        M1 --> E1["Eval Suite (12 Queries)"]:::process
        E1 --> QG{"Quality Gate<br/>Hit-Rate >= 75%?"}:::gate
        QG -- Pass --> R1["MLflow Registry<br/>(Production)"]:::gate
        QG -- Fail --> R2["Rollback"]:::monitor
    end

    subgraph S3 ["3. Deployment & Inference"]
        R1 --> API["FastAPI :8000"]:::process
        API --> SRCH["Similarity Search (Top-k)"]:::process
        SRCH --> GRND["Groundedness Check"]:::gate
        GRND --> UI["Streamlit UI :8501"]:::storage
    end

    subgraph S4 ["4. Closed-Loop Monitoring"]
        API --> PROM["Prometheus :8000/metrics"]:::monitor
        API --> LOGS["Query Audit Logs"]:::storage
        LOGS --> DRIFT{"Drift Detector<br/>Drop >= 30%?"}:::monitor
        DRIFT -- Drift Detected --> RETRAIN["Trigger Retraining"]:::monitor
    end

    RETRAIN -. Loop Trigger .-> D1
"""

with tab_arch:
    st.markdown(
        "<h3 style='font-size: 1.25rem; margin-bottom: 0.4rem;'>Closed-Loop MLOps System Architecture</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="pro-card">
            <p style="color: #d4d4d8; font-size: 0.95rem; margin: 0;">
                Interactive end-to-end architecture: Ingestion ➔ Experimentation ➔ Deployment ➔ Closed-loop Drift Monitoring.
                <em>(Use mouse drag to pan across nodes, wheel to zoom, or the top toolbar buttons).</em>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_mermaid_diagram(MLOPS_ARCHITECTURE_MERMAID, height=560)


# ----------------- Tab 1: Live Prometheus Telemetry -----------------
with tab_metrics:
    st.markdown("<h3 style='font-size: 1.25rem; margin-bottom: 0.4rem;'>Live Prometheus Telemetry Feeds</h3>",
                unsafe_allow_html=True)
    st.caption("Parsed in real-time from the running FastAPI backend (`/metrics`).")

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
                        .mark_bar(cornerRadius=3)
                        .encode(
                            x=alt.X("count:Q", title="Total Requests"),
                            y=alt.Y("endpoint:N", sort="-x", title="Endpoint"),
                            color=alt.Color(
                                "status:N",
                                scale=alt.Scale(domain=["ok", "error"], range=["#6366f1", "#f43f5e"]),
                            ),
                            tooltip=["endpoint", "status", "count"],
                        )
                        .properties(height=220)
                        .configure_axis(labelColor="#a1a1aa", titleColor="#71717a", labelFont="JetBrains Mono")
                    )
                    st.altair_chart(chart_req, use_container_width=True)
                else:
                    st.info("No request telemetry captured yet.")

            with c_m2:
                st.markdown("<h4 style='font-size: 1rem;'>Answer Status & Feedback Distributions</h4>", unsafe_allow_html=True)
                if ans_matches or fb_matches:
                    ans_data = [{"Metric": f"Answer: {m[0]}", "Count": float(m[1])} for m in ans_matches]
                    fb_data = [{"Metric": f"Feedback: {m[0]}", "Count": float(m[1])} for m in fb_matches]
                    df_dist = pd.DataFrame(ans_data + fb_data)

                    chart_dist = (
                        alt.Chart(df_dist)
                        .mark_bar(cornerRadius=3)
                        .encode(
                            x=alt.X("Count:Q", title="Total Observations"),
                            y=alt.Y("Metric:N", sort="-x", title="Distribution"),
                            color=alt.Color("Metric:N", scale=alt.Scale(scheme="indigo")),
                            tooltip=["Metric", "Count"],
                        )
                        .properties(height=220)
                        .configure_axis(labelColor="#a1a1aa", titleColor="#71717a", labelFont="JetBrains Mono")
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
    st.markdown("<h3 style='font-size: 1.25rem; margin-bottom: 0.4rem;'>Retrieval Gate Simulator</h3>",
                unsafe_allow_html=True)
    st.markdown(
        """
        <div class="pro-card">
            <p style="color: #d4d4d8; font-size: 0.95rem; margin: 0;">
                Test how the active retriever scores any arbitrary query. Inspect similarity score distributions,
                retrieved document chunk rank, and verify whether the threshold gate permits an answer or triggers refusal.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sim_q = st.text_input("Simulation Query String:", "How many days of paid sick leave do employees get?")

    if st.button("Run Retrieval Simulation", use_container_width=True):
        try:
            with st.spinner("Interrogating active index..."):
                r_sim = requests.post(f"{API}/ask", json={"question": sim_q}, timeout=30)
                if r_sim.ok:
                    res_sim = r_sim.json()
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Top Similarity Score", f"{res_sim.get('top_score', 0):.3f}")
                    c2.metric("Groundedness Confidence", f"{res_sim.get('groundedness', 0):.0%}")
                    c3.metric("Verdict", "ANSWERED" if res_sim.get("answered") else "REFUSED")

                    st.markdown("#### Retrieved Chunks & Similarity Ranks:")
                    sources = res_sim.get("sources", [])
                    if sources:
                        for s in sources:
                            st.markdown(
                                f"""
                                <div class="chunk-card">
                                    <div style="display: flex; justify-content: space-between; font-weight: 600; color: #818cf8;">
                                        <span>📄 {s.get('source')} (v{s.get('doc_version', 1)})</span>
                                        <span style="color: #34d399;">Score: {s.get('score', 0):.3f}</span>
                                    </div>
                                    <div style="color: #d4d4d8; font-size: 0.92rem; margin-top: 0.35rem; font-style: italic;">
                                        "{s.get('snippet', '')}"
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                    else:
                        st.warning("No candidate chunks exceeded the minimum similarity threshold. The assistant safely refused.")
                else:
                    st.error(r_sim.text)
        except Exception as e:
            st.error(f"Simulation failed: {e}")


# ----------------- Tab 4: Model & Data Governance -----------------
with tab_cards:
    st.markdown("<h3 style='font-size: 1.25rem; margin-bottom: 0.4rem;'>Responsible AI Governance</h3>",
                unsafe_allow_html=True)

    col_m, col_d = st.columns(2)

    with col_m:
        st.markdown("<h4 style='font-size: 1rem;'>Model Card (docs/model_card.md)</h4>", unsafe_allow_html=True)
        model_card_path = Path(_ROOT) / "docs" / "model_card.md"
        if model_card_path.exists():
            st.markdown(model_card_path.read_text(encoding="utf-8", errors="ignore"))
        else:
            st.info("docs/model_card.md not found.")

    with col_d:
        st.markdown("<h4 style='font-size: 1rem;'>Data Card (docs/data_card.md)</h4>", unsafe_allow_html=True)
        data_card_path = Path(_ROOT) / "docs" / "data_card.md"
        if data_card_path.exists():
            st.markdown(data_card_path.read_text(encoding="utf-8", errors="ignore"))
        else:
            st.info("docs/data_card.md not found.")
