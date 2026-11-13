"""API integration test with FastAPI's TestClient (needs an index: run `make pipeline` first, CI does)."""
import pytest
from fastapi.testclient import TestClient

from api.main import app, svc

client = TestClient(app)
pytestmark = pytest.mark.skipif(not svc.ready, reason="no index built")


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["index_loaded"] is True


def test_ask_returns_answer_with_sources():
    r = client.post("/ask", json={"question": "How do I reset my VPN token?"})
    body = r.json()
    assert r.status_code == 200 and body["answered"] and body["sources"]
    assert body["sources"][0]["source"] == "it_vpn_troubleshooting.md"


def test_ask_refuses_out_of_scope():
    body = client.post("/ask", json={"question": "Who won the cricket world cup?"}).json()
    assert body["answered"] is False


def test_input_validation():
    assert client.post("/ask", json={"question": "a"}).status_code == 422
    assert client.post("/ask", json={}).status_code == 422


def test_hr_endpoints_need_token():
    assert client.get("/admin/documents").status_code == 401
    assert client.get("/admin/documents", headers={"X-HR-Token": "hr-demo"}).status_code == 200


def test_metrics_endpoint():
    assert "ragops_requests_total" in client.get("/metrics/").text
