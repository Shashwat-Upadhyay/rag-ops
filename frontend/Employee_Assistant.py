"""Page 1 (default): Employee asks questions. Page 2 lives in pages/HR_Portal.py"""
import os

import requests
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")
st.set_page_config(page_title="Employee Assistant", page_icon="💬")
st.title("💬 Company Knowledge Assistant")
st.caption("Ask about HR, IT, finance or onboarding. Answers come only from verified company documents.")

st.session_state.setdefault("history", [])

question = st.chat_input("Ask a question, e.g. 'How many days of annual leave do I get?'")
if question:
    try:
        r = requests.post(f"{API}/ask", json={"question": question}, timeout=60)
        r.raise_for_status()
        st.session_state.history.append({"q": question, "res": r.json()})
    except requests.RequestException as e:
        st.error(f"Could not reach the assistant: {e}")

for i, item in enumerate(st.session_state.history):
    res = item["res"]
    with st.chat_message("user"):
        st.write(item["q"])
    with st.chat_message("assistant"):
        st.write(res["answer"])
        if res["answered"]:
            st.caption(f"Groundedness {res['groundedness']:.0%} · {res['latency_ms']} ms · prompt {res['prompt_version']}")
            with st.expander("Sources"):
                for s in res["sources"]:
                    st.markdown(f"**{s['source']}** (v{s['doc_version']}, score {s['score']})")
                    st.caption(s["snippet"])
        c1, c2, c3, _ = st.columns([1, 1, 2, 4])
        if c1.button("👍", key=f"up{i}"):
            requests.post(f"{API}/feedback", json={"helpful": True}, timeout=10)
            st.toast("Thanks!")
        if c2.button("👎", key=f"down{i}"):
            requests.post(f"{API}/feedback", json={"helpful": False}, timeout=10)
            st.toast("Thanks, HR will be notified.")
        if c3.button("Why this answer?", key=f"why{i}"):
            terms = requests.post(f"{API}/explain", json={"question": item["q"]}, timeout=60).json()["terms"]
            st.write("Words that helped find the match (LIME):")
            st.table({"word": [t["term"] for t in terms], "influence": [t["weight"] for t in terms]})
