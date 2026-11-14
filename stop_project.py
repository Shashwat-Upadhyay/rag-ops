"""Stops all running instances of the RAGOps platform (ports 8000 & 8501)."""
import subprocess


def stop_by_ports():
    ps_cmd = (
        "Get-NetTCPConnection -LocalPort 8000, 8501 -ErrorAction SilentlyContinue | "
        "Select-Object -ExpandProperty OwningProcess -Unique | "
        "ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=False)
    print("✅ All RAGOps backend (:8000) and frontend (:8501) services have been stopped.")


if __name__ == "__main__":
    stop_by_ports()
