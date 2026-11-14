"""Starts or verifies FastAPI backend (:8000) and launches Streamlit frontend (:8501)."""
import os
import subprocess
import time
import urllib.request
from pathlib import Path

_LOCAL_CACHE = (
    r"C:\Users\HP\AppData\Local\Packages"
    r"\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages"
)
root = Path(__file__).resolve().parent

env = os.environ.copy()
env["PYTHONPATH"] = f"{root / 'src'};{root};{env.get('PYTHONPATH', '')}"

print("==================================================", flush=True)
print("  🚀 STARTING RAG-OPS ENTERPRISE PLATFORM", flush=True)
print("==================================================", flush=True)


def is_api_running():
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=2) as response:
            return response.status == 200
    except Exception:
        return False


api_proc = None
if is_api_running():
    print("1. FastAPI Backend is already running on http://localhost:8000 [OK]", flush=True)
else:
    print("1. Launching FastAPI Backend on http://localhost:8000 ...", flush=True)
    api_cmd = (
        f"import site; site.addsitedir(r'{_LOCAL_CACHE}'); "
        "import uvicorn; uvicorn.run('api.main:app', host='127.0.0.1', port=8000)"
    )
    api_proc = subprocess.Popen(
        ["py", "-3.12", "-c", api_cmd],
        cwd=str(root),
        env=env,
    )
    for _ in range(10):
        time.sleep(1)
        if is_api_running():
            print("   FastAPI Backend started successfully [OK]", flush=True)
            break

print("2. Launching Streamlit Aurora Command UI on http://localhost:8501 ...", flush=True)
ui_proc = subprocess.Popen(
    ["py", "-3.12", str(root / "run_ui.py")],
    cwd=str(root),
    env=env,
)

print("\n✨ ALL SYSTEMS ONLINE & OPERATIONAL!", flush=True)
print("   - Frontend UI: http://localhost:8501", flush=True)
print("   - API Docs:    http://localhost:8000/docs", flush=True)
print("   - Metrics:     http://localhost:8000/metrics", flush=True)
print("==================================================", flush=True)

try:
    while True:
        if api_proc and api_proc.poll() is not None:
            print("API backend process terminated.", flush=True)
            break
        if ui_proc and ui_proc.poll() is not None:
            print("Streamlit UI process terminated.", flush=True)
            break
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    if api_proc:
        api_proc.terminate()
    if ui_proc:
        ui_proc.terminate()
