"""Convenience launcher for the RAGOps Streamlit Aurora Command UI."""
import sys
from pathlib import Path


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
