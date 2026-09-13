# Packet and ledger

Use a private directory outside the repo for operational files, with a separate
packet and output directory per invocation. Store no credentials, unrelated private
data, or full chat transcripts. Logs may contain source code: keep local, restrict
access, inspect/redact before quoting, and never commit or publish raw logs.

## Packet

Replace fields with real paths and commands; a few hundred words usually suffice.

```text
Task: T1 — [one observable outcome]
Working directory: [absolute repository path]
Inputs: [PRD/architecture/plan or brief paths and relevant sections]
Instructions: [applicable instruction files plus session-only constraints]
Baseline: [HEAD and private snapshot path; pre-existing changes to preserve]
Allowed changes: [explicit files/directories, including necessary tests]
Forbidden actions: [out-of-scope and unapproved external/git/DB actions]
Acceptance: [numbered observable success and failure cases]
Verification: [exact command arrays, working directories, expected results]
Known failures: [baseline evidence or none]
Budget: [time remaining, 2 routine repair rounds, any enforceable cost cap]

Implement only this task. Read instructions and relevant code.
Do not delegate further, modify this packet, or change the verification contract.
Run checks and fix routine code failures within budget. Do not weaken tests, skip
checks, add dependencies, or widen scope to obtain a pass.
Stop on tool/auth/permission blockers, design conflict, or exhausted budget.
No secrets in commands, reports, or logs. Return this short final report:

Status: ready_for_review | blocked
Changed files: [paths]
Checks: [actual commands, results, test counts where applicable]
Acceptance: [criterion -> evidence; explicitly state unmet cases]
Deviation/blocker: [reason or none]
Repair rounds used: [number]
Usage: [actual exposed token/cost figures or unknown]
```

The lead extracts the final report and exact session ID from tool output. The runner
does not normalize provider event schemas. If no exact ID can be established, use a
fresh session with the compact packet and correction context; never "continue last".

## Ledger

Maintain `ledger.md` as the compact recovery point:

```text
Feature / repositories:
Lead tool/model; worker profile/provider/model; verified CLI version:
Artifact and instruction paths:
Baseline HEAD; staged/unstaged diffs and untracked snapshot references:
Authorization boundaries / unresolved decisions:
Tasks: T1 [planned|running|blocked|review|accepted], dependencies, scope
Current packet / output directory / exact worker session ID:
Host process handle / process.json identity (PID, PGID, start time):
Worker repair rounds used / review correction rounds used:
Execution time used / remaining; measured cost / cap or unknown:
Verification evidence / lead review findings:
Next action:
```

On resumption, verify the old worker has stopped before launching another. Compare
current files against the baseline; do not rerun just because the ledger says
`running`. Preserve partial edits. Budgets persist across corrections/resumptions.
Use the host handle and recorded process identity to inspect liveness. PIDs can be
reused: confirm start time, command, and directory before signaling any process.
