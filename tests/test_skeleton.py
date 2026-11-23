"""The design entry point must not imply an implemented or externally run agent."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

CLI = Path(__file__).resolve().parents[1] / "scripts/run.py"
spec = importlib.util.spec_from_file_location("apm_skeleton", CLI)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class SkeletonBoundary(unittest.TestCase):
    def test_default_invocation_reports_unimplemented_instead_of_success(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(app.main([]), 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("not implemented", stderr.getvalue())
        self.assertIn("no intake, model call or section", stderr.getvalue())

    def test_status_is_explicit_design_metadata_not_a_draft(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(app.main(["--status"]), 0)
        status = json.loads(output.getvalue())
        self.assertEqual(status["name"], "APM Writing Assistant")
        self.assertEqual(status["implementation"], "skeleton")
        self.assertIs(status["can_draft"], False)
        self.assertIsNone(status["model_provider"])
        self.assertEqual(status["available_sections"], app.available_sections)
        self.assertNotIn("draft", status)

    def test_status_does_not_read_files_or_start_subprocesses(self):
        with mock.patch("builtins.open", side_effect=AssertionError("unexpected file read")), \
             mock.patch.object(subprocess, "Popen", side_effect=AssertionError("unexpected subprocess")), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(app.main(["--status"]), 0)

    def test_unknown_section_or_draft_options_are_not_silently_accepted(self):
        for args in [["--section", "2.6.1"], ["--draft"], ["../../output"]]:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as result:
                    app.main(args)
                self.assertEqual(result.exception.code, 2)

    def test_isolated_cli_needs_no_site_packages_and_ignores_local_env_and_modules(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sentinel = root / "unexpected-import"
            payload = "from pathlib import Path\nPath(" + repr(str(sentinel)) + ").touch()\nraise RuntimeError('synthetic module')\n"
            for name in ["anthropic", "openai", "streamlit", "dotenv", "sitecustomize"]:
                (root / (name + ".py")).write_text(payload)
            (root / ".env").write_text("ANTHROPIC_API_KEY=synthetic-not-a-real-key\n")
            before = {p.name for p in root.iterdir()}
            for args, code in [([], 2), (["--status"], 0)]:
                result = subprocess.run([sys.executable, "-I", "-S", str(CLI), *args], cwd=root,
                                        capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, code, result.stderr)
                if args:
                    self.assertFalse(json.loads(result.stdout)["can_draft"])
                self.assertEqual({p.name for p in root.iterdir()}, before)
                self.assertFalse(sentinel.exists())


if __name__ == "__main__":
    unittest.main()
