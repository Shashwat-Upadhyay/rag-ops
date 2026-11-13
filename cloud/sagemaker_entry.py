"""Runs inside the SageMaker container: executes the normal pipeline."""
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
subprocess.check_call([sys.executable, "-m", "ragops.pipeline"], env={"PYTHONPATH": "src:.", **__import__("os").environ})
