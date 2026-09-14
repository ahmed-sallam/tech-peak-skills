# Tech Peak Skills

Lean, composable agent skills for taking one feature from idea to reviewed delivery. Planning skills own individual stages, the QA skill verifies implemented behavior, and the delegation skill coordinates execution with your chosen coding tool and model.

## Workflow

```text
Idea
  ↓
PRD
  ↓
Architecture
  ↓
Plan
  ↓
Implementation
  ↓
QA / Tests
  ↓
Review
  ↓
Pull Request
```

This repository provides three planning skills, a QA skill, and an optional end-to-end coordinator:

| Skill | Question it answers | Default artifact |
| --- | --- | --- |
| `tp_prd` | What should we build? | `docs/prd/<feature-slug>.md` |
| `tp_architecture` | How should it fit the existing system? | `docs/architecture/<feature-slug>.md` |
| `tp_plan` | In what order should we implement it? | `docs/plans/<feature-slug>.md` |
| `tp-test` | Does the implemented behavior meet its requirements, and what evidence is missing? | `docs/qa/<feature-slug>.md` |
| `tp-delegate` | Who implements, how is work verified, and when is it accepted? | Planning artifacts + private task packets and execution evidence |

`tp-delegate` keeps the lead model responsible for decisions and review while a selected worker implements and fixes routine failures. Git writes, pull requests, and deployment still require the user's authorization.

## Install

Install all skills:

```bash
npx skills add https://github.com/ahmed-sallam/tech-peak-skills
```

Install one skill:

```bash
npx skills add https://github.com/ahmed-sallam/tech-peak-skills --skill tp_prd
npx skills add https://github.com/ahmed-sallam/tech-peak-skills --skill tp_architecture
npx skills add https://github.com/ahmed-sallam/tech-peak-skills --skill tp_plan
npx skills add https://github.com/ahmed-sallam/tech-peak-skills --skill tp-test
npx skills add https://github.com/ahmed-sallam/tech-peak-skills --skill tp-delegate
```

To install manually, copy the desired folder from `skills/` into your agent's project or global skills directory. Keep the folder name unchanged so it matches the skill's `name` metadata.

For Claude Code, use:

```text
.claude/skills/<skill-name>/     # project
~/.claude/skills/<skill-name>/   # global
```

## Skills

### `tp_prd`

Creates a short, buildable PRD for one feature from the current conversation and relevant codebase context. It defines the goal, scope, testable acceptance criteria, and concrete technical touchpoints without turning the document into an enterprise requirements exercise.

Use it when requirements need to be captured before architecture or implementation work begins.

### `tp_architecture`

Converts an approved PRD into a concise technical design for the existing codebase. It decides feature placement, reuse boundaries, data and API shape, integrations, security considerations, and important trade-offs without producing implementation tasks or code.

Use it before writing an implementation plan for architectural, cross-cutting, or high-risk features.

### `tp_plan`

Converts an approved PRD and architecture into an ordered implementation roadmap. It identifies concrete file changes, dependencies, validation steps, tests, risks, and checkpoints without revisiting product requirements or architectural decisions.

Use it when the design is settled and a coding agent needs an executable sequence of small, verifiable steps.

### `tp-test`

Runs a focused QA pass after implementation: inspect requirements and the diff, plan coverage, add missing tests, execute relevant checks, classify failures, and produce a report with a PASS, FAIL, or BLOCKED verdict. It leaves production-code fixes to the implementer unless you explicitly expand its scope.

It selects existing tools by risk: JUnit/Mockito for rules, Spring Boot Test/Testcontainers for persistence, existing API tests such as REST Assured or MockMvc, ArchUnit for established architecture rules, frontend unit/component tests, static checks, and Playwright for affected browser journeys. Other stacks reuse their established equivalents. Framework installation, CI changes, and active security scans are separate authorized work.

Playwright coverage focuses on affected routes, forms, permissions, and multi-step flows. Internal calculations do not automatically trigger browser tests. Missing E2E prerequisites remain visible as blocked evidence; mocked UI responses do not prove backend correctness. See [the skill](skills/tp-test/SKILL.md) and its conditional references.

Optional [SonarQube integration](skills/tp-test/references/sonarqube.md) reuses an authorized setup, verifies that analysis matches the tested revision, waits for server processing, and includes the Quality Gate and relevant findings in the QA report. If optional analysis is unavailable, the skill discloses the gap and continues; if project policy or the user requires it, missing evidence blocks acceptance. A completed matching gate failure is reported as FAIL. The skill does not install SonarQube, configure CI, or weaken quality rules automatically.

```text
Use $tp-test on the current feature diff and its acceptance criteria.
Add missing tests, run the relevant checks and affected Playwright journeys,
and write a QA report. Do not change production code or commit/push.
```

مثال عربي:

```text
استخدم $tp-test لاختبار ميزة تحصيل الرسوم بعد تنفيذها.
اقرأ المتطلبات والتغييرات، أضف الاختبارات الناقصة، وشغّل المناسب منها.
اختبر مسار المستخدم بـPlaywright وقواعد الحساب والحفظ في اختبارات مستقلة.
أعطني تقريرًا بالأخطاء والأدلة وما تعذّر اختباره، دون تعديل كود التطبيق أو الرفع.
```

The skill works standalone or as an explicitly assigned QA step in a `tp-delegate` workflow. It does not launch another agent automatically. Raw browser traces, authentication state, and sensitive logs belong outside version control. A QA report is evidence for review, not permission to merge or deploy.

### `tp-delegate`

Takes a feature through requirements, architecture, planning, delegated implementation, independent verification, correction, and delivery. Choose the worker tool and exact model in your request. OpenCode, Claude Code, Codex, and Pi profiles are included; other CLIs can be configured with a verified argument array.

Example request (replace the model placeholder with an ID available in your tool):

```text
Use $tp-delegate. Keep the current Codex/Astra session as lead.
Feature: add status/date filters to the request list using the existing API.
Prepare PRD, architecture, and plan, then delegate implementation to OpenCode
with model <verified-provider/model-id>.
Allow two worker repair rounds, one review correction, and 20 minutes per run.
Review and verify the final result. Do not commit or push.
```

مثال عربي:

```text
استخدم $tp-delegate من الفكرة للتسليم. خليك القائد في الجلسة الحالية.
المنفذ OpenCode والنموذج هو المعرّف المتاح الذي أحدده لك.
جهّز PRD وArchitecture وPlan، ثم سلّم التنفيذ وراجع واختبر الناتج.
اسمح بمحاولتي إصلاح للمنفذ وجولة تصحيح مراجعة واحدة، بدون commit أو push.
الفكرة: [وصف الميزة].
```

The lead's own model is selected in its host, not switched by the skill. Small tasks use one brief unless separate artifacts are requested. Existing Tech Peak planning skills are reused when available; concise equivalents work when only this skill is installed.

The bundled Python 3 runner needs no third-party packages and supports Linux/macOS. It offers a dry run, private logs, exact-session correction, timeout handling, and process-group cleanup. It does not enforce file scope or dollar/token budgets, automatically wake a closed lead task, or prove a model's completion claim. The lead keeps the host turn active, checks actual changes, and verifies acceptance. See [execution setup](skills/tp-delegate/references/execution.md).

CLI argument templates were checked against local help; real provider calls and account/model availability have not been tested. No particular model's price, quality, or availability is assumed.

## Validation

Run the offline runner tests (fake processes only, no model credits):

```bash
python3 -B -m unittest discover -s tests -v
```

## Naming and migration

The existing planning skills retain their `tp_` names. New skills `tp-delegate` and `tp-test` use hyphenated names for compatibility with skill validators; no existing skill is renamed. The testing skill discussed as `tp_test` is published as `tp-test`.

| Previous name | Current name |
| --- | --- |
| `prd` | `tp_prd` |
| `architecture` | `tp_architecture` |
| `tp_plan` | `tp_plan` |

If you installed an earlier version manually, remove the old `prd` and `architecture` skill folders after installing their renamed replacements.

## Design principles

- Give each planning skill one primary artifact; keep orchestration in the coordinator.
- Use repository context and existing conventions instead of inventing parallel structures.
- Keep requirements, architecture, planning, implementation, and review separate.
- Prefer concise, testable, implementation-ready outputs.
- State assumptions when missing information is not a genuine blocker.
