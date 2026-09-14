# SonarQube: optional analysis and Quality Gate

Use an existing, authorized SonarQube setup to supplement behavioral tests with
code-quality evidence. Do not install a server/scanner, configure credentials,
modify CI, or introduce dependencies merely because this skill is invoked.

## Decide applicability

Read project instructions and the user's request to determine whether SonarQube
is optional or required. A configuration file alone does not establish a mandatory
gate. Honor a request to exclude optional analysis; do not override project policy.

| Situation | Action and effect on the QA verdict |
| --- | --- |
| Optional and not configured | Continue the test plan; report not used and why. Absence alone does not block PASS. |
| Configured and authorized | Use existing matching evidence or execute the established analysis, then inspect its gate and findings. |
| Optional but unavailable, unauthorized, or unsupported for this target | Stop the affected operation without retries; disclose the gap and continue independent authorized tests. Do not claim SonarQube passed. |
| Required but unavailable, stale, pending past the deadline, or not computed | Mark the required check BLOCKED; the overall verdict is BLOCKED unless another confirmed failure makes it FAIL. |
| Completed, matching analysis with a failed gate | Report FAIL with the failed conditions and their scope; distinguish application defects from coverage or quality-policy failures. |
| Completed, matching analysis with a passed gate | Record that gate as passed; the overall verdict still depends on the other required criteria and checks. |

## Inspect setup before running

- Identify the configured server, project, scanner/build integration, installed
  versions, supported languages, and branch/PR capabilities. Verify commands and
  API fields against the repository or installed version's documentation.
- Confirm the target and permission to transmit this repository's source and
  analysis data. Configuration is not authorization to upload private code to a
  different server or cloud service. Reuse approved credentials without displaying
  tokens or embedding them in commands, logs, report URLs, or committed files.
- Check analysis scope, exclusions, new-code baseline, and existing quality policy.
  Do not redefine the baseline, loosen thresholds, exclude problem files, suppress
  findings, or mark security hotspots reviewed just to obtain a green result.
- Generate fresh coverage with the project's existing test tooling before analysis
  when coverage is expected. SonarQube imports coverage; it does not run the tests
  or generate that evidence. Verify report paths and imports, and distinguish
  missing coverage from measured zero coverage. Avoid borrowing reports from a
  different revision or a different test scope.

## Tie results to this QA run

Reuse a completed CI analysis only after verifying its project, branch/PR, revision,
and relevant scope. A main-branch dashboard does not prove the current feature or
local uncommitted changes were analyzed. For a local run, record the working-tree
state as well as HEAD and ensure it stays stable during analysis. If it changes,
mark the affected evidence stale rather than silently reporting PASS.

Follow the analysis identity returned by the established scanner/CI integration.
Server processing is asynchronous: successful scanner exit or report upload is
not a passed Quality Gate. Await processing and obtain the gate for that specific
analysis using the supported integration or verified API. Do not read an unrelated
"latest" gate that another concurrent scan may have replaced.

Use an existing project timeout or the user's budget; otherwise bound waiting to
five minutes. Wait at reasonable intervals through the host's process/event tools,
not repeated model launches. Stop immediately on processing failure, authentication,
permission, or connectivity errors; no blind resubmission. A pending result at the
deadline or an absent/not-computed gate is unavailable evidence, not a failed
application test and not a passing gate.

## Report actionable findings

Include the analysis identity, tested revision/scope, gate result and failed
conditions, safe evidence link, and relevant new-code issues in the QA report.
Keep old-code findings separate, but still disclose any overall-code condition
that fails the project's gate. Never infer that an issue is new from severity alone.
Review findings against actual code and requirements; security hotspots require
review and are not automatically confirmed vulnerabilities. Return application
fixes to the implementer within the skill's normal scope boundaries.

For editions without the needed branch/PR analysis, report that limitation. Do not
rename projects, relabel a feature as main, or install plugins as a workaround.
Future setup or policy changes are separate work; prefer discussing new-code gates
for an existing large codebase without applying that policy automatically.

## Official references

Consult only what the installed setup needs:

- [Analysis lifecycle and Community Build scope](https://docs.sonarsource.com/sonarqube-community-build/analyzing-source-code/analysis-overview)
- [Quality Gate conditions and new-code policy](https://docs.sonarsource.com/sonarqube-community-build/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates)
- [Java coverage import](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/test-coverage/java-test-coverage)
