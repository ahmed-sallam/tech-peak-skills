# Playwright: evidence for user journeys

Read the existing Playwright config, test scripts, project selection, fixtures,
authentication setup, base URL, and web-server startup/cleanup before execution.
Use the installed version and repository commands. Do not fabricate a `smoke`
project, tag, browser installation, or CI job; identify what actually exists.

Use browser CLI/MCP exploration when available to understand or reproduce a flow.
Exploration alone is not a durable regression suite: encode the important behavior
in the repository's test runner and execute it. If only exploration is possible,
report it as manual/agent-driven evidence and disclose the automated coverage gap.

## Choose the smallest useful journey

- Test the changed route/form/navigation and its important error state. Include
  affected authentication or role behavior and cross-step state when relevant.
- Use the existing smoke suite for basic availability and critical navigation.
  Full E2E is for a requested or justified regression pass, not every internal edit.
- If a supported browser or device mode is affected, include its configured project.
  Do not claim cross-browser coverage after running only Chromium.
- Follow applicable UI/UX review skills when assessing visual/accessibility behavior;
  do not restyle the app as part of QA. Add automated accessibility checks only with
  existing tooling; do not claim comprehensive accessibility compliance from them.

## Reliability and truthful coverage

- Prefer accessible roles/names, labels, and established test IDs. Use locators and
  state-based assertions supported by the installed runner; avoid fragile DOM paths
  and fixed sleeps. Wait for the observable event or result under test.
- Isolate browser contexts and synthetic users/data. Set up only the state needed
  by the journey; test login separately where session reuse bypasses it.
- Stub external services through existing test mechanisms. Declare mocked boundaries.
  A mocked payment/API response proves UI handling, not persisted payment correctness.
- For full integration evidence, exercise the test API/database path and verify
  persistence, reload, or downstream state where the requirement calls for it.
- Browser visibility of an action is not authorization enforcement. Pair UI permission
  cases with server-side denial and no-side-effect assertions at the API layer.
- Capture failure screenshots/traces/logs only with synthetic data and review before
  sharing. Auth storage state, cookies, tokens, and personal data must not be committed.
- Report timeouts, retries, skips, and flaky outcomes. Do not silently rerun until green.

## Missing environment

If browser binaries, server, credentials, or safe fixtures are missing, stop the
affected execution and report BLOCKED with its exact prerequisite. Do not download,
change permissions, reuse production accounts, or replace an integration test with
mocked evidence under the same claim. Retain any safe results already obtained.
