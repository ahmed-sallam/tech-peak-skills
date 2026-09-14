# QA report and implementation handoff

Produce one concise report in the user's language. Include only evidence necessary
to reproduce or assess results; link to sanitized details instead of dumping logs.

## Verdict

- **PASS**: all required in-scope criteria have sufficient executed evidence, required
  checks passed with actual tests discovered, and no unresolved in-scope failure remains.
- **FAIL**: at least one relevant check or criterion fails. Report whether the cause
  is the application, the test, pre-existing behavior, or still unknown. Also list
  blockers; a blocker must not hide a confirmed failure.
- **BLOCKED**: no confirmed failure, but a required check or criterion cannot be
  verified because prerequisites, authorization, or a requirement are unresolved.

A narrowed run can PASS only its explicitly stated scope. Read-only analysis or an
unexecuted test file cannot be reported as a passing automated test. Suspected flakes
remain unresolved; retries and pre-existing failures must stay visible.

## Include

1. **Scope and revision:** feature, acceptance source, repositories/HEADs, comparison
   base, relevant working-tree changes, environment, and date of execution.
2. **Coverage matrix:** criterion/risk → test path or identifier → layer → observed
   result. Distinguish verified, failed, blocked, and deliberately out-of-scope cases.
3. **Execution:** working directory, exact command, exit status, pass/fail/skip counts
   where exposed, and sanitized evidence path. Mark unavailable counts as unknown.
   Separate baseline from final runs and identify retries/stale or missing reports.
   When SonarQube applies, include whether it is optional/required, project and
   branch/PR, revision and analysis identity, completion time, Quality Gate result
   and failed conditions, and a safe result link. Distinguish unavailable analysis
   from a failed gate. Disclose stale evidence, missing coverage imports, and
   unverified working-tree changes; see [SonarQube guidance](sonarqube.md).
4. **Findings:** severity, affected location/test, minimal synthetic reproduction,
   expected versus observed outcome, user/data impact, and evidence. Distinguish
   confirmed defects from hypotheses; assign severity by impact, not the framework.
5. **Changes:** added/updated tests and fixtures, report path, and any approved scope
   expansion. Flag unexpected changes without overwriting someone else's work.
6. **Gaps and next action:** what was not verified and why, unresolved expectations,
   exact setup/approval needed, and the smallest implementation handoff.

Use severity consistently: critical for demonstrated severe exposure/data corruption,
high for a broken core flow or permission boundary, medium for meaningful limited
behavior loss, low for minor impact. Avoid speculative security claims.

## Handoff

For each actionable finding, provide the failing test/reproduction, requirement,
affected files, allowed implementation scope, and command needed to verify the fix.
Do not prescribe a broad refactor or silently delegate. Preserve evidence from the
failed revision and append results after a fix; green status refers to the tested revision.
