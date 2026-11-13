"""Page 2: HR uploads and manages policy documents. Every upload re-runs the pipeline."""
import os

import requests
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")
st.set_page_config(page_title="HR Portal", page_icon="📁")
st.title("📁 HR Portal")
st.caption("Upload policies and documentation. The assistant is rebuilt and tested automatically.")

token = st.sidebar.text_input("HR token", type="password", value=os.getenv("HR_TOKEN", ""))
headers = {"X-HR-Token": token}

files = st.file_uploader("Upload documents (PDF, Markdown or TXT)", type=["pdf", "md", "txt"],
                         accept_multiple_files=True)
if st.button("Upload & rebuild", disabled=not files):
    with st.spinner("Uploading, validating, indexing, evaluating…"):
        r = requests.post(f"{API}/admin/upload", headers=headers, timeout=600,
                          files=[("files", (f.name, f.getvalue())) for f in files])
    if r.ok:
        out = r.json()
        if out["promoted"]:
            st.success(f"Done. New index is live. Hit-rate {out['metrics'].get('hit_rate', 0):.0%}")
        else:
            st.warning("Documents saved but the new index FAILED the quality check, so the old index is still used.")
    else:
        st.error(r.json().get("detail", r.text))

st.subheader("Current documents")
r = requests.get(f"{API}/admin/documents", headers=headers, timeout=10)
if r.status_code == 401:
    st.info("Enter the HR token in the sidebar.")
elif r.ok:
    for name, info in r.json().items():
        c1, c2 = st.columns([5, 1])
        c1.write(f"**{name}**  ·  version {info['version']}  ·  updated {info['updated_at']}")
        if c2.button("Delete", key=name):
            requests.delete(f"{API}/admin/documents/{name}", headers=headers, timeout=600)
            st.rerun()
