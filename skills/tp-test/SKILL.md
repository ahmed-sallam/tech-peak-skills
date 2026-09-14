---
name: tp-test
description: Plan and execute focused QA for an implemented feature, bug fix, or diff. Derive cases from requirements, add missing tests, run relevant static, unit, integration, API, architecture, and Playwright checks, and report evidence and failures. Use for a QA pass or pre-PR testing; not feature implementation, a general code review, or an unsolicited full security audit.
---

# Tech Peak Test

Act as the QA agent. Verify observable requirements with repeatable tests owned by
the repository. Use its actual stack; Spring Boot and Next.js are common examples,
not prerequisites. A skill coordinates installed tools; it does not supply a test
runner, guarantee coverage, or automatically launch another coding agent.

## Boundaries

- Default scope: inspect code, add or improve relevant tests and test-only fixtures,
  execute authorized checks, and write one QA report. Honor a read-only request.
  Do not modify production code to make a test pass. Report defects to the implementer;
  change application code only if the user explicitly expands that scope.
- Read applicable project instructions and preserve existing changes. Git writes,
  migrations, CI/CD, dependencies, secrets, and external actions retain their own
  authorization requirements. Carry existing approvals forward; do not ask again.
- Before executing commands, inspect scripts, test profiles, service URLs, lifecycle
  hooks, and data setup/cleanup. Use isolated, disposable test data. An unfamiliar
  environment is not automatically safe because a command is named `test`.
- Do not point tests at production, send real payments/messages, use real personal
  data, or run active scans without authorization for that exact target and effect.
  Never expose credentials, session state, or private data in reports or artifacts.
- Reuse installed dependencies and verified commands. If a tool is missing, report
  the gap and propose setup separately; do not install it, pull images, download
  browsers, or change a lockfile without the authorization those actions require.

## 1. Establish scope and evidence

Read the user request, available PRD/acceptance criteria, relevant design, diff,
nearby implementation, and existing tests. Do not require planning documents for
a small task. Treat implementation behavior as evidence, not the specification.
If a business expectation is ambiguous, mark the affected criterion unresolved
and ask only what is needed; continue independent checks.

Record repository/HEAD, staged and unstaged changes, untracked files, and the exact
comparison base when supplied. Do not guess a branch or mix unrelated changes into
the feature. For an unspecified local pass, describe the working-tree scope; if
there is no identifiable change, ask for the feature or comparison target.

Inspect build manifests, scripts, test discovery patterns, fixtures, profiles, and
existing result locations. Verify command syntax against the installed tool or
repository; never invent flags, framework versions, or configuration keys.

## 2. Make a compact test plan

Before edits, map each acceptance criterion or material risk to a test layer,
existing/missing test, expected outcome, command, and prerequisites. Include normal,
boundary, and failure cases where meaningful; avoid copying implementation branches
into assertions. List dependency-ordered subtasks with verification for larger work.

| Change or risk | Preferred evidence, using existing tooling |
| --- | --- |
| Pure rules, validation, calculations | Unit tests; JUnit/Mockito for Java, existing frontend runner such as Vitest |
| Persistence, queries, transactions, rollback | Integration tests; Spring Boot Test/Testcontainers or the project's isolated database setup |
| API input/output, auth, tenant/role boundaries | API/integration tests; existing MockMvc, REST Assured, or equivalent |
| Module dependency or layering rules | Existing ArchUnit rules or equivalent; do not invent architecture policy |
| Components and local UI states | Existing component tests; add browser coverage for affected user behavior |
| Routes, forms, browser auth, permissions, multi-step user flows | Playwright E2E for the affected journey, plus lower-layer checks for its rules |
| Build, types, formatting/lint, static rules | Relevant existing build/typecheck/lint/static-analysis commands |
| Configured code-quality policy | Optional SonarQube analysis and Quality Gate for the tested revision |

Use the lowest layer that proves each property. Internal service/mapper/calculation
changes normally need no browser run. Browser-visible behavior requires targeted
E2E evidence; prefer Playwright when present. Preserve an established equivalent
runner rather than add a second one without approval. If E2E cannot run, record
the missing evidence; a unit test or mocked browser response cannot prove full integration.

Read [Playwright guidance](references/playwright.md) only for browser work.
Read [business and backend cases](references/backend.md) for persistence, API,
financial, permission, or architectural changes.
Read [SonarQube guidance](references/sonarqube.md) when SonarQube is configured,
explicitly requested, or required by project policy. Use it when available and
authorized; optional absence is a disclosed gap, while missing required evidence
blocks acceptance. It supplements the behavioral tests above.

Default to affected tests and the relevant existing smoke suite. Run full E2E or
repository-wide expensive checks when requested, required by project policy, or
justified by impact. Record why broader checks were omitted. Suggest scheduled
full runs only as a recommendation; never edit CI or create schedules implicitly.
Contract fuzzing, load tests, and active security scans are conditional work,
not mandatory phases of an ordinary feature QA pass.

## 3. Add tests and execute

Reuse fixtures and conventions. Assert requirements and durable outcomes, including
negative cases; avoid tests that merely repeat mocks, snapshots, or implementation.
For a reproducible bug, capture a failing regression first unless explicitly waived.
Keep it failing if application code is defective; a red test can be a valid QA result.

Run a relevant baseline before additions where feasible, then the new/affected
tests, integration checks, and required broader verification. Record commands,
working directories, exit status, discovered/executed counts, skips, and evidence
paths. A successful command with zero matching tests, skipped checks, or stale
reports is not a pass. Separate pre-existing failures from newly observed failures;
do not claim provenance without baseline evidence.

Run sequentially unless tasks have independent files, fixtures, databases, ports,
and other runtime resources. Parallel flags alone do not establish isolation.
Capture only necessary, sanitized logs and browser artifacts; keep sensitive raw
artifacts out of version control. Clean up only resources this run owns.

## 4. Diagnose without hiding failures

Classify failures as application defect, test defect, environment/tooling blocker,
pre-existing failure, or suspected flakiness. State uncertainty where unresolved.
Do not weaken assertions, skip failures, increase retries to hide instability,
refresh snapshots blindly, or call a later green retry a clean first pass.

Fix test defects only when evidence shows the test contradicts the requirement.
Allow at most two test-repair rounds per issue, or a stricter user/project limit.
Stop immediately on environment/auth/permission blockers, safety concerns, or
design/scope conflicts; do not retry or widen access. Preserve partial results
and identify the smallest next action. For code/test failures, stop at the limit
and report attempts. Rerun only after a justified change or authorized diagnostic.

## 5. Report and hand back

Use the project's QA report location, otherwise `docs/qa/<feature-slug>.md`.
Use a stable, non-sensitive slug. Preserve prior evidence; do not overwrite an
unrelated report. For read-only work, return the report inline. Follow
[report format](references/report.md); keep detail proportional to the task.

Re-read the entire QA diff and check scope, meaningful assertions, missing cases,
and sensitive artifacts. Report what ran, what did not, unresolved criteria, and
actual required approvals. A completed QA pass can have a FAIL or BLOCKED verdict.
Do not equate test success with production readiness or approval to merge.

Provide an implementation handoff containing reproducible findings and relevant
test paths. If delegation is explicitly requested, use an available coordinator
such as `tp-delegate`, preserving the selected tool/model and permissions. Otherwise
return the handoff to the user; do not launch models or send messages automatically.
After an authorized fix, rerun the affected checks and update evidence on that revision.
