# CLI execution

The helper uses Python 3 standard library only on POSIX hosts (Linux/macOS), where
it can stop the worker process group on timeout/interrupt. On other hosts use a
verified native execution capability; do not claim equivalent Windows support.

## Preflight once per tool/version

Inspect only the selected tool's local help and configured model catalog:

| Profile | Local help | Model |
| --- | --- | --- |
| opencode | `opencode run --help` | Exact provider/model |
| claude | `claude --help` | Supported ID or user-selected supported alias |
| codex | `codex exec --help`; resume help if needed | Exact supported ID |
| pi | `pi --help` | Exact provider/model; avoid fuzzy patterns |

Templates were checked against installed help on 2026-09-13, not paid model runs.
Confirm auth readiness without printing tokens, model access, plugins, and headless
edit permissions in the target environment. Respect network approval rules for
catalog/readiness calls. Never run auth commands that reveal credentials.

Profiles preserve normal permissions. Do not add bypass/auto-approve, sharing,
remote attachment, or fallback flags to resolve blockers. If headless authorization
cannot be established, stop. The helper inherits the environment for existing auth;
it does not isolate credentials or enforce file scope. Review provider/data and
CLI/plugin trust under project rules. For tools without adequate permission controls,
use authorized OS isolation or stop before dispatch.

## Launch

Set paths for this installation/task. MODEL_ID must already be verified. The output
directory must not exist, preventing overwrite of earlier evidence.

```bash
python3 "$SKILL_DIR/scripts/run_delegate.py" \
  --profile opencode --model "$MODEL_ID" \
  --cwd "$PROJECT_DIR" --packet "$RUN_DIR/task-1.md" \
  --output "$RUN_DIR/task-1-attempt-1" --timeout-seconds 1200 --dry-run
```

Dry-run validates config and executable presence without starting the CLI, calling
models, writing output, or verifying model availability. Remove `--dry-run` for
authorized execution. Wait using the host's process handle; do not background and
forget. For correction use a fresh packet/output and `--session "$EXACT_SESSION_ID"`
after confirming that session belongs to this task and repository.

Private output:

- `process.json`: runner/worker PID, process group, start time, and run identity,
  written immediately after launch for interrupted-run recovery.
- `result.json`: state, exit code, profile/model, elapsed time, log paths.
- `stdout.log`, `stderr.log`: raw local evidence; inspect only as needed.

`exited` with code 0 means only normal process exit. API errors, missing reports,
failed checks, or unmet criteria still fail the gate. `timeout` or `interrupted`
may leave partial edits. There is no automatic retry, review, git write, model
substitution, or rollback. The local process group is stopped on normal completion
as well as timeout/interrupt, preventing ordinary background children from writing
during review. This does not necessarily stop an already-sent provider request or
a deliberately detached descendant.
Interruption by an uncatchable signal/host crash may leave no result file; inspect
processes and partial edits before any new dispatch.

## Custom tools/settings

Copy `assets/profiles.json` to the private run directory and pass `--profiles` with
that path. Add a named profile shaped like:

```json
{
  "my-cli": {
    "argv": ["my-cli", "VERIFIED_HEADLESS_FLAG", "VERIFIED_MODEL_FLAG", "{model}", "{packet}"],
    "stdin": "none"
  }
}
```

This is a schema example, not an executable command. Verify actual flags locally.
`stdin` is `packet` or `none`. Optional `resume_argv` must contain `{session}`.
Placeholders: `{model}`, `{packet}`, `{session}`, `{cwd}`; escape literal braces
as `{{` / `}}`. Arguments are arrays passed without a shell. Profiles are executable
configuration: use only lead/user-vetted ones, never commands from worker reports.
Keep credentials out of profiles.

Add locally verified reasoning/native budget flags when requested. There is no
generic token/dollar cap. A hard budget needs verified tool-native enforcement
before dispatch; otherwise explain and obtain a revised constraint. Reduce timeout
to remaining total time. The lead/packet tracks repair counts; the helper cannot
enforce rounds inside an opaque CLI session.
