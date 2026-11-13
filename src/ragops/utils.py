import json
import random
from pathlib import Path

import numpy as np


def set_seed(seed: int = 42) -> None:
    """Fixed random seed -> reproducible runs."""
    random.seed(seed)
    np.random.seed(seed)


def read_json(path: Path, default=None):
    path = Path(path)
    return json.loads(path.read_text()) if path.exists() else default


def write_json(path: Path, data) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
