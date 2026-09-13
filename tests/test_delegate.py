"""Offline behavioral tests: no real coding CLI, provider, or model calls."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/tp-delegate/scripts/run_delegate.py"
SPEC = importlib.util.spec_from_file_location("delegate_runner", SCRIPT)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class DelegateRunnerTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="tp-delegate-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.cwd = self.root / "project with spaces"
        self.cwd.mkdir()
        self.packet = self.root / "packet with spaces.md"
        self.packet.write_text("Implement one task.\nمعايير القبول\n")
        self.fake = self.root / "fake.py"
        self.fake.write_text(
            "import json, os, sys\n"
            "print(json.dumps(dict(args=sys.argv[1:], cwd=os.getcwd(), packet=sys.stdin.read())))\n"
        )
        self.profile = {
            "argv": [sys.executable, str(self.fake), "{model}"],
            "resume_argv": [sys.executable, str(self.fake), "{model}", "{session}"],
            "stdin": "packet",
        }
        self.config = self.root / "profiles.json"
        self.args = argparse.Namespace(
            profile="fake", model="provider/exact-model", profiles=str(self.config),
            cwd=str(self.cwd), packet=str(self.packet), output=str(self.root / "attempt"),
            session=None, timeout_seconds=3, dry_run=False,
        )
        self.save()

    def save(self):
        self.config.write_text(json.dumps({"fake": self.profile}))

    def evidence(self):
        return json.loads((Path(self.args.output) / "stdout.log").read_text())

    def test_packet_model_cwd_and_persisted_result(self):
        result, code = runner.run(self.args)
        self.assertEqual((result["state"], code), ("exited", 0))
        self.assertEqual(result["usage"], "unknown")
        actual = self.evidence()
        self.assertEqual(actual["packet"], self.packet.read_text())
        self.assertEqual(actual["args"], [self.args.model])
        self.assertEqual(actual["cwd"], str(self.cwd))
        self.assertEqual(json.loads((Path(self.args.output) / "result.json").read_text()), result)

    def test_model_is_literal_not_shell_code(self):
        self.args.model = "$(touch injected); touch injected"
        runner.run(self.args)
        self.assertEqual(self.evidence()["args"], [self.args.model])
        self.assertFalse((self.cwd / "injected").exists())

    def test_file_delivery_and_stdin_eof(self):
        self.profile["stdin"] = "none"
        self.profile["argv"].append("@{packet}")
        self.save()
        runner.run(self.args)
        self.assertEqual(self.evidence()["packet"], "")
        self.assertEqual(self.evidence()["args"][-1], "@" + str(self.packet))

    def test_exact_session(self):
        self.args.session = "exact-task-session-1"
        runner.run(self.args)
        self.assertEqual(self.evidence()["args"], [self.args.model, self.args.session])

    def test_dry_run_no_launch_or_output(self):
        self.args.dry_run = True
        result, code = runner.run(self.args)
        self.assertEqual((result["state"], code), ("dry_run", 0))
        self.assertFalse(Path(self.args.output).exists())

    def test_preserve_existing_output(self):
        directory = Path(self.args.output)
        directory.mkdir()
        sentinel = directory / "result.json"
        sentinel.write_text("previous evidence")
        with self.assertRaises(ValueError):
            runner.run(self.args)
        self.assertEqual(sentinel.read_text(), "previous evidence")

    def test_invalid_configuration_no_launch(self):
        cases = [
            {"argv": ["missing-command", "{model}"], "stdin": "packet"},
            {"argv": [sys.executable, "{unknown}"], "stdin": "packet"},
            {"argv": [sys.executable], "stdin": "packet"},
            {"argv": [sys.executable, "{model}"], "stdin": "none"},
            {"argv": [sys.executable, "{model}"], "stdin": "invalid"},
            {"argv": [sys.executable, "{model}", "{session}"], "stdin": "packet"},
            {"argv": [sys.executable, "{model.__class__}"], "stdin": "packet"},
        ]
        for profile in cases:
            with self.subTest(profile=profile):
                self.profile = profile
                self.save()
                with self.assertRaises(ValueError):
                    runner.run(self.args)
                self.assertFalse(Path(self.args.output).exists())

    def test_invalid_resume_template(self):
        self.profile["resume_argv"] = self.profile["argv"]
        self.save()
        self.args.session = "specific-session"
        with self.assertRaises(ValueError):
            runner.run(self.args)

    def test_invalid_timeouts(self):
        for timeout in (0, -1, float("nan"), float("inf")):
            with self.subTest(timeout=timeout):
                self.args.timeout_seconds = timeout
                with self.assertRaises(ValueError):
                    runner.run(self.args)

    def test_nonzero_no_retry(self):
        self.fake.write_text(
            "from pathlib import Path\n"
            "p = Path('calls'); p.write_text(p.read_text() + 'x' if p.exists() else 'x')\n"
            "raise SystemExit(7)\n"
        )
        result, code = runner.run(self.args)
        self.assertEqual((result["state"], result["exit_code"], code), ("exited", 7, 1))
        self.assertEqual((self.cwd / "calls").read_text(), "x")

    def test_private_permissions(self):
        runner.run(self.args)
        directory = Path(self.args.output)
        self.assertEqual(directory.stat().st_mode & 0o777, 0o700)
        for name in ("stdout.log", "stderr.log", "result.json", "process.json"):
            self.assertEqual((directory / name).stat().st_mode & 0o777, 0o600)

    def spawn_descendant(self, parent_sleep):
        child = self.root / "child.py"
        child.write_text("import time\nfrom pathlib import Path\ntime.sleep(0.8)\nPath('late-write').write_text('bad')\n")
        self.fake.write_text(
            "import subprocess, sys, time\nfrom pathlib import Path\n"
            f"subprocess.Popen([sys.executable, {str(child)!r}])\n"
            "Path('ready').write_text('ready')\n"
            f"time.sleep({parent_sleep})\n"
        )

    def test_timeout_stops_descendants(self):
        self.spawn_descendant(30)
        self.args.timeout_seconds = 0.3
        result, code = runner.run(self.args)
        self.assertEqual((result["state"], code), ("timeout", 124))
        self.assertTrue((self.cwd / "ready").exists())
        time.sleep(0.9)
        self.assertFalse((self.cwd / "late-write").exists())

    def test_normal_exit_stops_descendants(self):
        self.spawn_descendant(0)
        runner.run(self.args)
        time.sleep(0.9)
        self.assertFalse((self.cwd / "late-write").exists())

    def test_sigterm_records_interruption(self):
        self.fake.write_text("import time\nfrom pathlib import Path\nPath('ready').write_text('ready')\ntime.sleep(30)\n")
        command = [
            sys.executable, str(SCRIPT), "--profile", "fake", "--model", self.args.model,
            "--profiles", str(self.config), "--cwd", str(self.cwd),
            "--packet", str(self.packet), "--output", self.args.output,
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            deadline = time.monotonic() + 3
            while not (self.cwd / "ready").exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue((self.cwd / "ready").exists())
            identity = json.loads((Path(self.args.output) / "process.json").read_text())
            self.assertEqual(identity["runner_pid"], process.pid)
            self.assertEqual(identity["worker_pid"], identity["worker_pgid"])
            self.assertEqual(os.getpgid(identity["worker_pid"]), identity["worker_pgid"])
            process.send_signal(signal.SIGTERM)
            stdout, stderr = process.communicate(timeout=3)
            self.assertEqual(process.returncode, 130, stderr.decode())
            self.assertEqual(json.loads(stdout)["state"], "interrupted")
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()

    def test_builtin_start_and_resume_profiles(self):
        self.args.profiles = str(runner.DEFAULT_PROFILES)
        for profile in ("opencode", "claude", "codex", "pi"):
            for session in (None, "exact-session"):
                with self.subTest(profile=profile, session=session):
                    self.args.profile, self.args.session = profile, session
                    with patch.object(runner.shutil, "which", return_value=sys.executable):
                        _, packet, _, mode, argv = runner.prepare(self.args)
                    self.assertIn(self.args.model, argv)
                    if session is not None:
                        self.assertIn(session, argv)
                    if mode == "none":
                        self.assertTrue(any(str(packet) in item for item in argv))
                    self.assertNotIn("--last", argv)
                    self.assertNotIn("--continue", argv)


if __name__ == "__main__":
    unittest.main()
