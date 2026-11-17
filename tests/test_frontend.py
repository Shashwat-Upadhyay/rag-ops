"""Frontend regressions runnable without Streamlit or a running API."""
import ast
import json
from pathlib import Path
import runpy
import sys
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


class State(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


class FrontendTests(unittest.TestCase):
    def test_ui_launcher_invokes_streamlit(self):
        cli = MagicMock()
        captured = []
        cli.main.side_effect = lambda: captured.extend(sys.argv) or 0
        web = MagicMock()
        web.cli = cli
        with patch.dict(sys.modules, {"streamlit": MagicMock(), "streamlit.web": web}), patch.object(sys, "argv", ["run_ui.py"]):
            with self.assertRaises(SystemExit) as caught:
                runpy.run_path(str(ROOT / "run_ui.py"), run_name="__main__")
            self.assertEqual(caught.exception.code, 0)
            cli.main.assert_called_once_with()
            self.assertEqual(captured[:2], ["streamlit", "run"])
            self.assertEqual(Path(captured[2]), FRONTEND / "Employee_Assistant.py")

    def setUp(self):
        self.st = MagicMock()
        self.st.session_state = State()
        self.st.columns.side_effect = lambda spec: [self.column() for _ in range(spec if isinstance(spec, int) else len(spec))]
        self.st.tabs.side_effect = lambda labels: [MagicMock() for _ in labels]
        self.st.button.return_value = False
        self.st.chat_input.return_value = None
        self.st.text_input.return_value = ""
        self.st.file_uploader.return_value = []
        self.st.cache_data.side_effect = lambda **kwargs: lambda fn: fn
        self.components = MagicMock()
        self.st.components.v1 = self.components
        self.http = MagicMock()
        self.http.RequestException = RuntimeError
        self.http.API_URL = "http://test"
        self.http.document_url.side_effect = lambda name: "http://test/admin/documents/" + name
        self.health = {"status": "no_index", "retriever": None, "index_version": None, "documents": {}}
        self.http.get.return_value.json.return_value = self.health
        self.modules = {"streamlit": self.st, "streamlit.components": MagicMock(),
                        "streamlit.components.v1": self.components, "api_client": self.http,
                        "pandas": MagicMock(), "altair": MagicMock()}

    def column(self):
        column = MagicMock()
        column.button.return_value = False
        return column

    def run_page(self, path):
        with patch.dict(sys.modules, self.modules), patch.object(sys, "path", [str(FRONTEND)] + sys.path):
            sys.modules.pop("theme", None)
            return runpy.run_path(str(FRONTEND / path))

    def test_employee_without_index(self):
        self.run_page("Employee_Assistant.py")
        self.assertTrue(any("administrator needs to build" in str(c) for c in self.st.info.call_args_list))
        self.assertTrue(any("Index not ready" in str(c) for c in self.st.markdown.call_args_list))

    def test_failed_drift_is_unavailable(self):
        response = MagicMock()
        response.json.return_value = self.health
        self.http.get.side_effect = [response, RuntimeError("offline")]
        self.run_page("Employee_Assistant.py")
        markup = str(self.st.markdown.call_args_list)
        self.assertIn("Unavailable", markup)
        self.assertNotIn("Zero Drift", markup)

    def test_answer_escapes_markup_and_reports_real_score(self):
        self.st.session_state.history = [{"q": "<img src=x>", "res": {
            "answered": True, "groundedness": .85, "answer": "<script>alert(1)</script>",
            "sources": [{"source": "<img>", "snippet": "<iframe>"}]}}]
        self.run_page("Employee_Assistant.py")
        markup = str(self.st.markdown.call_args_list)
        self.assertIn("85%", markup)
        self.assertNotIn("100% Grounded", markup)
        self.assertIn("&lt;script&gt;", markup)
        self.assertNotIn("<script>alert(1)</script>", markup)

    def test_hr_starts_without_credentials(self):
        self.run_page("pages/HR_Portal.py")
        self.st.sidebar.text_input.assert_called_once_with("HR Token", type="password", key="hr_token")
        self.http.delete.assert_not_called()
        self.http.post.assert_not_called()

    def test_hr_reports_missing_server_configuration(self):
        self.st.sidebar.text_input.return_value = "entered-token"
        error = RuntimeError("503")
        error.response = MagicMock(status_code=503)
        self.http.get.side_effect = error
        self.run_page("pages/HR_Portal.py")
        self.assertIn("not configured on the API server", str(self.st.sidebar.error.call_args_list))

    def test_backend_loads_project_env_before_reading_token(self):
        tree = ast.parse((ROOT / "api/main.py").read_text(encoding="utf-8"))
        nodes = [n for n in tree.body if (
            isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
            and isinstance(n.value.func, ast.Name) and n.value.func.id == "load_dotenv"
        ) or (isinstance(n, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "HR_TOKEN" for t in n.targets
        ))]
        environment = {}
        loader = MagicMock(side_effect=lambda *a, **kw: environment.update(HR_TOKEN="test-file-token"))
        os_mock = MagicMock()
        os_mock.getenv.side_effect = environment.get
        scope = {"load_dotenv": loader, "Path": Path, "__file__": str(ROOT / "api/main.py"), "os": os_mock}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), "env_setup", "exec"), scope)
        loader.assert_called_once_with(ROOT / ".env", override=False)
        self.assertEqual(scope["HR_TOKEN"], "test-file-token")

    def test_feedback_failure_does_not_record_vote(self):
        item = {"q": "Annual leave?", "res": {"answered": False}}
        self.st.session_state.history = [item]
        self.st.button.side_effect = lambda label, **kwargs: kwargs.get("key") == "up_0"
        self.http.post.side_effect = RuntimeError("500")
        self.run_page("Employee_Assistant.py")
        self.assertNotIn("feedback", item)
        self.assertEqual(self.st.session_state.positive_feedback, 0)

    def test_existing_vote_cannot_be_submitted_again(self):
        self.st.session_state.history = [{"q": "Annual leave?", "res": {"answered": False}, "feedback": True}]
        self.st.button.side_effect = lambda label, **kwargs: kwargs.get("key") == "up_0"
        self.run_page("Employee_Assistant.py")
        self.http.post.assert_not_called()

    def test_delete_requires_confirmation(self):
        self.st.sidebar.text_input.return_value = "entered-token"
        self.st.text_input.return_value = ""
        response = MagicMock()
        response.json.return_value = {"policy.md": {"version": 1}}
        self.http.get.return_value = response
        self.st.button.side_effect = lambda label, **kwargs: kwargs.get("key") == "del_policy.md"
        self.run_page("pages/HR_Portal.py")
        self.http.delete.assert_not_called()
        self.assertEqual(self.st.session_state.pending_delete, "policy.md")

    def test_script_literal_and_metric_escape(self):
        with patch.dict(sys.modules, self.modules):
            theme = runpy.run_path(str(FRONTEND / "theme.py"))
        payload = '</script><script>alert("x")</script>\\\n'
        literal = theme["script_literal"](payload)
        self.assertNotIn("<", literal)
        self.assertEqual(json.loads(literal), payload)
        theme["render_audio_briefing"](payload, "voice_1")
        audio = self.components.html.call_args.args[0]
        self.assertNotIn(payload, audio)
        theme["render_animated_metric"]("<img>", payload)
        metric = self.components.html.call_args.args[0]
        self.assertIn("&lt;img&gt;", metric)
        self.assertNotIn(payload, metric)

    def test_http_errors_are_raised_and_filename_encoded(self):
        transport = MagicMock()
        transport.RequestException = RuntimeError
        with patch.dict(sys.modules, {"requests": transport}):
            client = runpy.run_path(str(FRONTEND / "api_client.py"))
            transport.request.return_value.raise_for_status.side_effect = RuntimeError("500")
            with self.assertRaises(RuntimeError):
                client["post"]("http://test/feedback", json={"helpful": True})
            self.assertTrue(client["document_url"]("a #?.md").endswith("a%20%23%3F.md"))

    def test_admin_fails_closed_without_configured_token(self):
        tree = ast.parse((ROOT / "api/main.py").read_text(encoding="utf-8"))
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_require_hr")
        class HTTPError(Exception):
            def __init__(self, status, detail):
                self.status = status
        import secrets
        scope = {"HR_TOKEN": None, "HTTPException": HTTPError, "secrets": secrets}
        exec(compile(ast.Module(body=[node], type_ignores=[]), "auth", "exec"), scope)
        with self.assertRaises(HTTPError) as caught:
            scope["_require_hr"]("hr-demo")
        self.assertEqual(caught.exception.status, 503)
        scope["HR_TOKEN"] = "test-only-secret"
        with self.assertRaises(HTTPError) as caught:
            scope["_require_hr"]("wrong")
        self.assertEqual(caught.exception.status, 401)
        scope["_require_hr"]("test-only-secret")


if __name__ == "__main__":
    unittest.main()
