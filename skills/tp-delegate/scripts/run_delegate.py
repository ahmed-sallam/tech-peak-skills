#!/usr/bin/env python3
"""Run one vetted headless coding CLI; report process evidence, never acceptance."""

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import shutil
import signal
import string
import subprocess
import time


DEFAULT_PROFILES = Path(__file__).resolve().parent.parent / "assets" / "profiles.json"


def prepare(args):
    if os.name != "posix":
        raise ValueError("POSIX process-group control is required")
    if not math.isfinite(args.timeout_seconds) or args.timeout_seconds <= 0:
        raise ValueError("timeout must be finite and positive")
    if not args.model.strip() or args.model.startswith("-"):
        raise ValueError("an explicit model ID is required")
    if args.session is not None and (
        not args.session.strip() or args.session.startswith("-")
    ):
        raise ValueError("session must be an explicit ID, not an option")
    cwd = Path(args.cwd).resolve(strict=True)
    packet = Path(args.packet).resolve(strict=True)
    output = Path(args.output).absolute()
    if not cwd.is_dir() or not packet.is_file():
        raise ValueError("cwd must be a directory and packet must be a file")
    if output.exists() or output.is_symlink():
        raise ValueError("output already exists; use a fresh attempt path")
    profiles = json.loads(Path(args.profiles).read_text(encoding="utf-8"))
    if not isinstance(profiles, dict):
        raise ValueError("profiles must be a JSON object")
    profile = profiles.get(args.profile)
    if not isinstance(profile, dict):
        raise ValueError("unknown or invalid profile")
    if set(profile) - {"argv", "resume_argv", "stdin"}:
        raise ValueError("unknown profile fields")
    mode = profile.get("stdin")
    if mode not in ("packet", "none"):
        raise ValueError("stdin must be packet or none")
    template = profile.get("resume_argv" if args.session is not None else "argv")
    if not isinstance(template, list) or not template or not all(
        isinstance(item, str) and item for item in template
    ):
        raise ValueError("missing or invalid argv template")
    values = {
        "model": args.model, "packet": str(packet),
        "session": args.session, "cwd": str(cwd),
    }
    fields = set()
    for item in template:
        for _, field, spec, conversion in string.Formatter().parse(item):
            if field is not None:
                if field not in values or spec or conversion:
                    raise ValueError("unsupported template placeholder")
                fields.add(field)
    if "model" not in fields:
        raise ValueError("template must select the requested model")
    if mode == "none" and "packet" not in fields:
        raise ValueError("template must deliver the packet")
    if args.session is not None and "session" not in fields:
        raise ValueError("resume template must select the exact session")
    if args.session is None and "session" in fields:
        raise ValueError("session placeholder requires --session")
    argv = [item.format_map(values) for item in template]
    if any("\x00" in item for item in argv):
        raise ValueError("NUL is not allowed in arguments")
    if "/" in argv[0] and not Path(argv[0]).is_absolute():
        raise ValueError("executable must be an absolute path or PATH command")
    executable = shutil.which(argv[0])
    if executable is None:
        raise ValueError("configured executable is unavailable")
    argv[0] = str(Path(executable).resolve())
    return cwd, packet, output, mode, argv


def stop_group(process):
    # Descendants may remain even when the leader has just exited.
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass  # The process group has already exited.
    process.wait()


def interrupted(_signum, _frame):
    raise KeyboardInterrupt


def run(args):
    cwd, packet, output, mode, argv = prepare(args)
    result = {
        "state": "dry_run", "profile": args.profile, "model": args.model,
        "session": args.session, "cwd": str(cwd), "exit_code": None,
        "elapsed_seconds": 0, "usage": "unknown",
    }
    if args.dry_run:
        return result, 0
    output.mkdir(mode=0o700, parents=True, exist_ok=False)
    os.chmod(output, 0o700)
    stdout_path, stderr_path = output / "stdout.log", output / "stderr.log"
    result.update(stdout=str(stdout_path), stderr=str(stderr_path))
    started = time.monotonic()
    process = None
    previous_handlers = {
        sig: signal.signal(sig, interrupted) for sig in (signal.SIGINT, signal.SIGTERM)
    }
    try:
        with packet.open("rb") as source, stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
            os.chmod(stdout_path, 0o600)
            os.chmod(stderr_path, 0o600)
            process = subprocess.Popen(
                argv, cwd=cwd,
                stdin=source if mode == "packet" else subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, start_new_session=True,
            )
            identity = {
                "runner_pid": os.getpid(), "worker_pid": process.pid,
                "worker_pgid": process.pid,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "cwd": str(cwd), "profile": args.profile, "model": args.model,
            }
            with (output / "process.json").open("x", encoding="utf-8") as handle:
                os.chmod(output / "process.json", 0o600)
                json.dump(identity, handle, indent=2)
                handle.write("\n")
            result["exit_code"] = process.wait(timeout=args.timeout_seconds)
            stop_group(process)
            result["state"] = "exited"
            code = 0 if result["exit_code"] == 0 else 1
    except subprocess.TimeoutExpired:
        stop_group(process)
        result.update(state="timeout", exit_code=process.returncode)
        code = 124
    except KeyboardInterrupt:
        if process is not None:
            stop_group(process)
        result.update(
            state="interrupted", exit_code=process.returncode if process else None
        )
        code = 130
    except OSError as error:
        if process is not None:
            stop_group(process)
        result.update(state="launch_error", error_errno=error.errno)
        code = 1
    finally:
        for sig, handler in previous_handlers.items():
            signal.signal(sig, handler)
    result["elapsed_seconds"] = round(time.monotonic() - started, 3)
    result_path = output / "result.json"
    with result_path.open("x", encoding="utf-8") as handle:
        os.chmod(result_path, 0o600)
        json.dump(result, handle, indent=2)
        handle.write("\n")
    return result, code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--profiles", default=str(DEFAULT_PROFILES))
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--packet", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--session")
    parser.add_argument("--timeout-seconds", type=float, default=1200)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        result, code = run(args)
    except (ValueError, OSError):
        parser.exit(2, "Preflight/output error: check profile, paths, model, timeout, and executable; no retry performed.\n")
    print(json.dumps(result))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
