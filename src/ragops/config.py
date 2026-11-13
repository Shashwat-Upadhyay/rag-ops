"""Load configs/config.yaml. All paths are resolved relative to the project root."""
import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_config() -> dict:
    cfg_path = Path(os.getenv("RAGOPS_CONFIG", ROOT / "configs" / "config.yaml"))
    cfg = yaml.safe_load(cfg_path.read_text())
    # Optional: run only some experiments, e.g. RAGOPS_EXPERIMENTS=baseline_tfidf (used in CI)
    only = os.getenv("RAGOPS_EXPERIMENTS")
    if only:
        names = {n.strip() for n in only.split(",")}
        cfg["experiments"] = [e for e in cfg["experiments"] if e["name"] in names]
    cfg["paths"] = {k: ROOT / v for k, v in cfg["paths"].items()}
    return cfg


def load_prompts() -> dict:
    return yaml.safe_load((ROOT / "configs" / "prompts.yaml").read_text())
