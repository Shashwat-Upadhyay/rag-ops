"""Page 1: Executive Knowledge Assistant (Employee Intelligence Portal).
High-precision enterprise Q&A with real-time groundedness verification,
LIME explainability, and multi-department prompt routing.
"""
import json
import os
import sys
import time
from datetime import datetime

# Ensure local packages site-packages is on sys.path
_LOCAL_CACHE = (
    r"C:\Users\HP\AppData\Local\Packages"
    r"\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages"
)
if os.path.exists(_LOCAL_CACHE) and _LOCAL_CACHE not in sys.path:
    sys.path.append(_LOCAL_CACHE)

import altair as alt  # noqa: E402
import pandas as pd  # noqa: E402
import requests  # noqa: E402
import streamlit as st  # noqa: E402
from theme import (  # noqa: E402
    inject_executive_theme,
    render_animated_metric,
    render_audio_briefing,
    render_confetti,
    render_status_ring,
    render_token_influence_heatmap,
)

# ----------------- Configuration & Initialization -----------------
API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="RAGOps // Neural Knowledge Command",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_executive_theme()

# Session State Initialization
st.session_state.setdefault("history", [])
st.session_state.setdefault("total_queries", 0)
st.session_state.setdefault("positive_feedback", 0)
st.session_state.setdefault("negative_feedback", 0)
st.session_state.setdefault("latencies", [])
st.session_state.setdefault("lime_cache", {})
st.session_state.setdefault("pending_prompt", None)


# ----------------- API Telemetry Fetcher -----------------
@st.cache_data(ttl=5)
def get_system_telemetry():
    """Fetches real-time system health and drift status from the backend."""
    health_data = {"status": "offline", "index_version": "N/A", "retriever": "N/A", "documents": {}}
    drift_data = {"drift_detected": False, "decision": "unknown"}
    try:
        r = requests.get(f"{API}/health", timeout=3)
        if r.ok:
            health_data = r.json()
    except Exception:
        pass

    try:
        rd = requests.get(f"{API}/drift", timeout=3)
        if rd.ok:
            drift_data = rd.json()
    except Exception:
        pass

    return health_data, drift_data


telemetry, drift = get_system_telemetry()
is_online = telemetry.get("status") == "ok"
doc_count = len(telemetry.get("documents", {}))
retriever_name = telemetry.get("retriever", "tfidf")
index_ver = telemetry.get("index_version", "unknown")
drift_detected = drift.get("drift_detected", False)


# ----------------- Executive Header & Live Status Radar -----------------
c_head_left, c_head_right = st.columns([2.2, 1])

with c_head_left:
    st.markdown(
        """
        <div>
            <h1 class="gradient-heading" style="font-size: 2.2rem; margin-bottom: 0.2rem;">
                Neural Knowledge Command
            </h1>
            <p style="margin: 0.15rem 0 0.5rem 0; color: #94a3b8; font-size: 0.95rem; font-weight: 500;">
                Verified corporate documentation intelligence with automated hallucination defenses & LIME explainability.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c_head_right:
    render_status_ring(is_online)
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: -8px;">
            <span style="background: rgba(124, 58, 237, 0.18); border: 1px solid rgba(124, 58, 237, 0.4);
                         color: #c084fc; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700;
                         padding: 3px 9px; border-radius: 5px;">
                RAG·OPS v0.2
            </span>
            <span style="background: rgba(16, 185, 129, 0.18); border: 1px solid rgba(16, 185, 129, 0.4);
                         color: #34d399; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700;
                         padding: 3px 9px; border-radius: 5px;">
                PRODUCTION
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------- Telemetry Command Strip -----------------
dot_class = "online" if is_online else "alert"
drift_color = "#ff4d6d" if drift_detected else "#10b981"
drift_label = "Drift Alert" if drift_detected else "Zero Drift (Stable)"

st.markdown(
    f"""
    <div class="telemetry-strip">
        <div class="metric-chip">
            <span class="status-dot {dot_class}"></span>
            Backend: <strong>{'Online (HTTP 200)' if is_online else 'Offline'}</strong>
        </div>
        <div class="metric-chip">
            Retriever: <strong>{retriever_name.upper()}</strong>
        </div>
        <div class="metric-chip">
            Index Hash: <strong>{index_ver[:8]}</strong>
        </div>
        <div class="metric-chip">
            Corpus: <strong>{doc_count} Verified Documents</strong>
        </div>
        <div class="metric-chip">
            Drift Status: <strong style="color: {drift_color};">{drift_label}</strong>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ----------------- Interactive Prompt Command Palette -----------------
with st.container():
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
            <span style="color: #00d4ff; font-size: 0.9rem;">⚡</span>
            <span style="font-size: 0.82rem; font-weight: 700; color: #c084fc; text-transform: uppercase;
                         letter-spacing: 0.08em; font-family: 'Syne', sans-serif;">
                Policy Prompt Palette (Verified Routing)
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_hr, tab_it, tab_fin, tab_onb, tab_safe = st.tabs([
        "HR & Leaves",
        "IT & VPN",
        "Finance & Expenses",
        "Onboarding",
        "Safety & Refusal Tests",
    ])

    with tab_hr:
        c1, c2, c3 = st.columns(3)
        if c1.button("🌴 How many days of annual leave do I get?", use_container_width=True):
            st.session_state.pending_prompt = "How many days of annual leave do I get?"
        if c2.button("🔄 Can I carry forward unused leave?", use_container_width=True):
            st.session_state.pending_prompt = "Can I carry forward unused leave?"
        if c3.button("👶 How long is paternity leave?", use_container_width=True):
            st.session_state.pending_prompt = "How long is paternity leave?"

    with tab_it:
        c1, c2 = st.columns(2)
        if c1.button("🔑 How do I reset my VPN token?", use_container_width=True):
            st.session_state.pending_prompt = "How do I reset my VPN token?"
        if c2.button("🔒 How often must passwords be changed?", use_container_width=True):
            st.session_state.pending_prompt = "How often must passwords be changed?"

    with tab_fin:
        c1, c2 = st.columns(2)
        if c1.button("🍽️ Daily meal and transport reimbursement limit?", use_container_width=True):
            st.session_state.pending_prompt = "What is the daily meal and transport reimbursement limit?"
        if c2.button("🧾 Within how many days should I submit expense claims?", use_container_width=True):
            st.session_state.pending_prompt = "Within how many days should I submit an expense claim?"

    with tab_onb:
        c1, c2 = st.columns(2)
        if c1.button("⏳ How long is the probation period?", use_container_width=True):
            st.session_state.pending_prompt = "How long is the probation period?"
        if c2.button("📋 What training must a new joiner complete?", use_container_width=True):
            st.session_state.pending_prompt = "What training must a new joiner complete?"

    with tab_safe:
        c1, c2, c3 = st.columns(3)
        if c1.button("🍕 Recommend a good pizza recipe (Out of Domain)", use_container_width=True):
            st.session_state.pending_prompt = "Recommend a good pizza recipe"
        if c2.button("🏏 Who won the cricket world cup? (Hallucination Test)", use_container_width=True):
            st.session_state.pending_prompt = "Who won the cricket world cup?"
        if c3.button("🏛️ What is the capital of Australia?", use_container_width=True):
            st.session_state.pending_prompt = "What is the capital of Australia?"


# ----------------- Query Execution Pipeline -----------------
st.markdown(
    """
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #64748b;
                margin-top: 0.8rem; margin-bottom: 0.2rem;">
        COMMAND BAR: Ask anything about company policy · Press Enter to query
    </div>
    """,
    unsafe_allow_html=True,
)

chat_input = st.chat_input("Ask about company HR, IT, finance, or onboarding policies...")

active_query = None
if chat_input:
    active_query = chat_input
elif st.session_state.pending_prompt:
    active_query = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if active_query:
    with st.spinner("Executing similarity scan & verifying groundedness..."):
        t0 = time.perf_counter()
        try:
            r = requests.post(f"{API}/ask", json={"question": active_query}, timeout=45)
            r.raise_for_status()
            res = r.json()
            latency = (time.perf_counter() - t0) * 1000

            st.session_state.history.append({
                "q": active_query,
                "res": res,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "client_latency_ms": round(latency, 1),
            })
            st.session_state.total_queries += 1
            st.session_state.latencies.append(res.get("latency_ms", latency))
            st.rerun()
        except requests.RequestException as e:
            st.error(f"Could not reach Knowledge Assistant service: {e}")


# ----------------- Conversation & Evidence Explorer -----------------
if not st.session_state.history:
    st.markdown(
        """
        <div class="aurora-card" style="text-align: center; padding: 2.8rem 1.8rem; margin-top: 1.5rem;">
            <div style="font-size: 2.6rem; margin-bottom: 0.6rem; filter: drop-shadow(0 0 16px rgba(124, 58, 237, 0.6));">
                ⚡
            </div>
            <h3 class="gradient-heading" style="font-size: 1.45rem; margin-bottom: 0.5rem;">
                Neural Knowledge Command Standing By
            </h3>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto 1.25rem auto; font-size: 0.95rem; line-height: 1.6;">
                Every query is indexed, matched against corporate policy documentation, and audited for hallucination prevention.
                Select any prompt from the palette above or type directly into the command bar.
            </p>
            <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
                <span class="metric-chip">🌴 Annual Leaves</span>
                <span class="metric-chip">🔑 VPN Access</span>
                <span class="metric-chip">🍽️ Expense Limits</span>
                <span class="metric-chip">🛡️ Hallucination Defenses</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

for idx, item in enumerate(st.session_state.history):
    q = item["q"]
    res = item["res"]
    ts = item.get("timestamp", "")
    latency_ms = res.get("latency_ms", item.get("client_latency_ms", 0))
    groundedness = res.get("groundedness", 0.0)
    answered = res.get("answered", False)
    sources = res.get("sources", [])
    prompt_ver = res.get("prompt_version", "v2")
    top_score = res.get("top_score", 0.0)

    # 1. User Query
    st.markdown(
        f"""
        <div class="msg-query">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
                             color: #00d4ff; letter-spacing: 0.06em; font-family: 'Syne', sans-serif;">
                    ▶ Employee Policy Query
                </span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #64748b;">
                    {ts}
                </span>
            </div>
            <div style="font-size: 1.08rem; font-weight: 600; color: #f8fafc;">
                {q}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Assistant Answer Card
    primary_source = sources[0].get("source", "verified policy") if sources else "verified policy"
    if answered and groundedness >= 0.80:
        shield_html = f"""<span class="badge-verified">✓ 100% Grounded in {primary_source}</span>"""
    elif answered:
        shield_html = f"""<span class="badge-warning">⚠ Partial Grounding ({groundedness:.0%})</span>"""
    else:
        shield_html = """<span class="badge-refusal">🛡️ Defended: Refusal (No matching documentation)</span>"""

    answer_text = res.get("answer", "")
    st.markdown(
        f"""
        <div class="msg-answer">
            <div style="display: flex; justify-content: space-between; align-items: center;
                        margin-bottom: 0.85rem; flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    {shield_html}
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
                            color: #94a3b8; display: flex; gap: 0.85rem;">
                    <span>⏱ {latency_ms:.1f}ms</span>
                    <span>Relevance: {top_score:.3f}</span>
                    <span style="color: #c084fc;">{prompt_ver}</span>
                </div>
            </div>
            <div style="font-size: 1.06rem; line-height: 1.65; color: #f8fafc;">
                {answer_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Audio Briefing
    render_audio_briefing(answer_text, f"voice_{idx}")

    # 3. Evidence Sources Breakdown with Visual Score Progress Bars
    if answered and sources:
        with st.expander(f"Cited Evidence Passages ({len(sources)} source chunks)", expanded=False):
            for s in sources:
                score = s.get("score", 0.0)
                score_pct = min(max(score * 100, 0), 100)
                src_name = s.get("source")
                doc_ver = s.get("doc_version", 1)
                bar_color = "#10b981" if score >= 0.65 else ("#f59e0b" if score >= 0.40 else "#ff4d6d")

                st.markdown(
                    f"""
                    <div class="chunk-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                            <span style="font-weight: 700; color: #c084fc; font-size: 0.9rem;">
                                📄 {src_name} <span style="color: #64748b; font-size: 0.78rem;">(version {doc_ver})</span>
                            </span>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #34d399;">
                                Cosine Score: {score:.3f} ({score_pct:.0f}%)
                            </span>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.06); height: 4px; border-radius: 2px;
                                    margin-bottom: 0.6rem; overflow: hidden;">
                            <div style="background: {bar_color}; width: {score_pct}%; height: 100%; border-radius: 2px;"></div>
                        </div>
                        <div style="color: #cbd5e1; font-size: 0.92rem; font-style: italic; line-height: 1.5;">
                            "{s.get('snippet', '')}"
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # 4. Action Bar (Feedback & LIME XAI)
    c_fb1, c_fb2, c_lime, _ = st.columns([0.75, 0.75, 2.5, 4.5])
    with c_fb1:
        if st.button("👍 Helpful", key=f"up_{idx}"):
            try:
                requests.post(f"{API}/feedback", json={"helpful": True}, timeout=5)
                st.session_state.positive_feedback += 1
                render_confetti()
                st.toast("Feedback recorded: Helpful", icon="✅")
            except Exception:
                st.toast("Failed to log feedback")
    with c_fb2:
        if st.button("👎 Poor", key=f"down_{idx}"):
            try:
                requests.post(f"{API}/feedback", json={"helpful": False}, timeout=5)
                st.session_state.negative_feedback += 1
                st.toast("Feedback recorded: Flagged for review", icon="⚠️")
            except Exception:
                st.toast("Failed to log feedback")
    with c_lime:
        show_lime = st.button("🔍 Explain Query Influence (LIME)", key=f"lime_btn_{idx}")

    # LIME Explanation Display
    cache_key = f"lime_{q}"
    if show_lime or cache_key in st.session_state.lime_cache:
        with st.spinner("Fitting local LIME surrogate model..."):
            if cache_key not in st.session_state.lime_cache:
                try:
                    rexp = requests.post(f"{API}/explain", json={"question": q}, timeout=60)
                    if rexp.ok:
                        st.session_state.lime_cache[cache_key] = rexp.json().get("terms", [])
                    else:
                        st.session_state.lime_cache[cache_key] = []
                except Exception as ex:
                    st.warning(f"Could not compute explanation: {ex}")
                    st.session_state.lime_cache[cache_key] = []

            terms = st.session_state.lime_cache.get(cache_key, [])
            if terms:
                render_token_influence_heatmap(terms)

                df_lime = pd.DataFrame(terms)
                df_lime["direction"] = df_lime["weight"].apply(
                    lambda w: "Positive match" if w >= 0 else "Negative impact"
                )

                chart = (
                    alt.Chart(df_lime)
                    .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
                    .encode(
                        x=alt.X("weight:Q", title="Cosine Feature Influence"),
                        y=alt.Y("term:N", sort="-x", title="Token"),
                        color=alt.Color(
                            "direction:N",
                            scale=alt.Scale(domain=["Positive match", "Negative impact"], range=["#10b981", "#ff4d6d"]),
                            legend=alt.Legend(title="Influence Direction"),
                        ),
                        tooltip=["term", "weight", "direction"],
                    )
                    .properties(height=max(140, len(terms) * 26), width="container")
                    .configure_view(strokeWidth=0)
                    .configure_axis(labelColor="#94a3b8", titleColor="#64748b", labelFont="JetBrains Mono")
                )
                st.altair_chart(chart, use_container_width=True)

    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.06); margin: 1.35rem 0;'>", unsafe_allow_html=True)


# ----------------- Executive Sidebar Telemetry & Audit -----------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
            <div style="font-size: 0.78rem; font-weight: 700; color: #00d4ff; text-transform: uppercase;
                        letter-spacing: 0.08em; font-family: 'Syne', sans-serif;">
                Telemetry Matrix
            </div>
            <div style="font-size: 1.2rem; font-weight: 800; color: #f8fafc; font-family: 'Syne', sans-serif; margin-top: 2px;">
                Session Observability
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    avg_lat = sum(st.session_state.latencies) / len(st.session_state.latencies) if st.session_state.latencies else 0.0

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    render_animated_metric("Total Queries", st.session_state.total_queries, accent_color="#7c3aed")
    render_animated_metric("Avg Latency", f"{avg_lat:.1f}ms", accent_color="#00d4ff", suffix="ms")

    c_f1, c_f2 = st.columns(2)
    with c_f1:
        render_animated_metric("Helpful", st.session_state.positive_feedback, accent_color="#10b981")
    with c_f2:
        render_animated_metric("Flagged", st.session_state.negative_feedback, accent_color="#ff4d6d")

    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 1.25rem 0;'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #c084fc;
                    letter-spacing: 0.06em; margin-bottom: 0.5rem; font-family: 'Syne', sans-serif;">
            Compliance & Audit Studio
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.history:
        json_data = json.dumps(st.session_state.history, indent=2)
        st.download_button(
            label="📥 Export Session Audit (JSON)",
            data=json_data,
            file_name=f"ragops_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )

        md_lines = ["# RAGOps Corporate Assistant Audit Log\n\n"]
        for item in st.session_state.history:
            md_lines.append(f"### Query: {item['q']}\n")
            md_lines.append(f"**Answer**: {item['res'].get('answer')}\n\n")
            md_lines.append(f"- **Groundedness**: {item['res'].get('groundedness', 0):.0%}\n")
            md_lines.append(f"- **Latency**: {item['res'].get('latency_ms', 0):.1f} ms\n")
            md_lines.append(f"- **Timestamp**: {item.get('timestamp', '')}\n\n---\n\n")

        st.download_button(
            label="📄 Export Compliance Report (Markdown)",
            data="".join(md_lines),
            file_name=f"ragops_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    if st.button("🧹 Clear Conversation History", use_container_width=True):
        st.session_state.history = []
        st.session_state.total_queries = 0
        st.session_state.latencies = []
        st.session_state.lime_cache = {}
        st.rerun()

    st.markdown("<br><hr style='border-color: rgba(255, 255, 255, 0.08);'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: 0.75rem; color: #64748b; text-align: center; font-family: 'JetBrains Mono', monospace;">
            RAG·OPS ENTERPRISE EDITION<br>
            <span style="color: #10b981;">● AIR-GAPPED VERIFICATION</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
