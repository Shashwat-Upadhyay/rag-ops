"""Quality gate + prediction tests. Runs the real pipeline on the sample documents (TF-IDF only)."""
import pytest

from ragops import pipeline
from ragops.config import load_config
from ragops.index import Index


@pytest.fixture(scope="module")
def cfg(tmp_path_factory):
    cfg = load_config()
    tmp = tmp_path_factory.mktemp("run")
    # write outputs to a temp dir so tests never touch real data/index or mlflow.db
    for k in ("processed_dir", "candidates_dir", "index_dir", "registry", "metrics_file"):
        cfg["paths"][k] = tmp / cfg["paths"][k].name
    cfg["mlflow"]["tracking_uri"] = f"sqlite:///{tmp}/mlflow.db"
    return cfg


def test_pipeline_passes_quality_gate(cfg):
    assert pipeline.run_all(cfg) is True          # fails if hit_rate / decision_accuracy < thresholds


def test_prediction_finds_right_document(cfg):
    idx = Index.load(cfg["paths"]["index_dir"], cfg)
    top = idx.search("How many days of annual leave do I get?")[0]
    assert top["source"] == "hr_leave_policy.md"


def test_out_of_scope_question_has_low_score(cfg):
    idx = Index.load(cfg["paths"]["index_dir"], cfg)
    assert idx.top_score("What is the capital of Australia?") < idx.exp["min_score"]
