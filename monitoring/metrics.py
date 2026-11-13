"""Prometheus metrics exposed by the API at /metrics."""
from prometheus_client import Counter, Gauge, Histogram

REQUESTS = Counter("ragops_requests_total", "HTTP requests", ["endpoint", "status"])
LATENCY = Histogram("ragops_request_latency_seconds", "Request latency", ["endpoint"],
                    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10))
ANSWERS = Counter("ragops_answers_total", "Prediction distribution", ["outcome"])  # answered | no_answer
TOP_SCORE = Histogram("ragops_top_retrieval_score", "Best retrieval score per question",
                      buckets=(0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0))
GROUNDEDNESS = Histogram("ragops_groundedness", "Answer groundedness (0..1)",
                         buckets=(0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0))
FEEDBACK = Counter("ragops_feedback_total", "Employee feedback (actual labels)", ["label"])  # up | down
DRIFT = Gauge("ragops_drift_detected", "1 if drift detected on recent queries")
INDEX_DOCS = Gauge("ragops_indexed_documents", "Number of documents in the live index")
