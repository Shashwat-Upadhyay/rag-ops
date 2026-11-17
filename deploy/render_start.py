"""Run the internal API and public Streamlit service on Render's assigned port."""
import os
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    if not os.environ.get("HR_TOKEN"):
        raise RuntimeError("Set HR_TOKEN in Render's Environment settings before deploying.")
    env = os.environ.copy()
    env["API_URL"] = "http://127.0.0.1:8000"
    children = []

    def stop(*_):
        for child in reversed(children):
            if child.poll() is None:
                child.terminate()
        for child in children:
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                child.kill()

    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))
    try:
        api = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=ROOT, env=env,
        )
        children.append(api)
        for _ in range(120):
            if api.poll() is not None:
                raise RuntimeError("Internal API failed during startup; inspect the preceding logs.")
            try:
                import json
                with urllib.request.urlopen(env["API_URL"] + "/health", timeout=2) as response:
                    if json.load(response).get("index_loaded"):
                        break
            except OSError:
                pass
            time.sleep(1)
        else:
            raise RuntimeError("API did not become ready with an index within 120 seconds.")
        children.append(subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "frontend/Employee_Assistant.py",
            "--server.address", "0.0.0.0", "--server.port", os.environ.get("PORT", "10000"),
            "--server.headless", "true", "--browser.gatherUsageStats", "false",
        ], cwd=ROOT, env=env))
        while all(child.poll() is None for child in children):
            time.sleep(1)
        raise RuntimeError("An application process exited unexpectedly.")
    finally:
        stop()


if __name__ == "__main__":
    main()
