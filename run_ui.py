"""Convenience launcher for the RAGOps Streamlit Cyberpunk UI."""
import os
import sys
from pathlib import Path

# Add site-packages if on Windows Store Python setup
_LOCAL_CACHE = (
    r"C:\Users\HP\AppData\Local\Packages"
    r"\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages"
)
if os.path.exists(_LOCAL_CACHE) and _LOCAL_CACHE not in sys.path:
    import site
    site.addsitedir(_LOCAL_CACHE)

root_dir = Path(__file__).resolve().parent
frontend_script = root_dir / "frontend" / "Employee_Assistant.py"

if __name__ == "__main__":
    from streamlit.web import cli as stcli
    sys.argv = [
        "streamlit",
        "run",
        str(frontend_script),
        "--server.port",
        "8501",
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]
    sys.exit(stcli.main())
