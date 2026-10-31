---
name: tdd
description: Drive test-first feature implementation or bug fixes through Red, Green, Refactor using meaningful unit and integration tests. Use when the user requests TDD or tests before implementation; honor tests-only handoffs. Not a post-implementation QA pass.
---

# Tech Peak TDD

Implement one observable behavior at a time: prove a test fails, make it pass,
then refactor with tests green. Derive expectations from requirements and agreed
contracts, not from the current implementation. Do not write the entire feature's
test suite before learning from the first implementation cycle.

## Scope and workflow

- Work within the user's authorized implementation scope. If asked for tests only,
  write and run the failing tests, report the handoff, and stop before production
  changes. Include required scaffolding in the agreed scope; do not silently add it.
- In a planned feature, follow `tp_prd` -> `tp_architecture` -> `tp_plan` ->
  `tdd` with implementation -> `tp-test` for final QA, when those skills are
  installed. Recognize legacy planning names `prd` and `architecture`. Small
  tasks need only a clear behavior and acceptance criteria, not three documents.
- `tp-delegate` can coordinate this workflow. Put the TDD requirement and evidence
  in its worker packet; keep the tests and implementation with the same authorized
  writer. Do not launch another agent or change the chosen tool/model implicitly.
- Reuse installed runners, fixtures, and conventions. Tests must use isolated,
  disposable data. Inspect scripts, hooks, service targets, and cleanup before
  execution; stop on unsafe or unknown targets, missing tools, or permissions.
  Dependency installation, downloads, schema migrations, CI, and external writes
  remain separate actions requiring the applicable authorization.

## 1. Establish the next behavior

Read applicable instructions, relevant source/tests, requirements, and available
architecture/plan. Inspect repository status and preserve pre-existing changes.
Verify test commands and discovery against project scripts/configuration. Run the
relevant existing baseline before edits; record failures without assuming their
cause. Stop on environment/tooling blockers rather than treating them as Red.

Choose a small behavior and state its input, observable result, and important
boundary or failure case. Map it to the lowest test layer that proves the property:

| Property | Test evidence |
| --- | --- |
| Rules, validation, calculations, state transitions in isolation | Unit tests with concrete inputs and outcomes |
| Queries, mappings, constraints, transactions, persistence | Integration tests exercising the real repository/database boundary in an isolated test environment |
| API routing, validation, serialization, component wiring | Integration tests through the project's actual application test harness |

Use both unit and integration tests when they prove different relevant risks;
do not require both for every behavior. A mocked repository cannot prove database
constraints or rollback. Name mocked boundaries and limit claims accordingly.
For a persistence or wiring change, plan the corresponding integration test before
implementing that behavior. Browser/E2E tests complement these layers when needed;
they do not replace the requested unit or integration evidence.

If a required contract or business outcome is unresolved, ask before encoding it
as an assertion. Do not invent public interfaces or business rules to unblock TDD.

## 2. Red: prove the missing behavior

Write a focused test, or a small cohesive set, for the next behavior before its
production logic. For a bug, first reproduce the reported defect with a regression.
Reuse public interfaces and assert durable results rather than private methods,
incidental call order, implementation snapshots, or mocks merely echoing setup.

Run the exact new tests and confirm they were discovered and executed. Inspect
the failure and record the unmet expectation. If missing symbols prevent execution,
add only authorized minimal scaffolding, then rerun to reach a behavioral failure.
Syntax/import errors, broken fixtures, unavailable databases, and zero tests are
not proof of Red. If the test already passes, investigate existing coverage or an
incorrect test assumption; do not change working code just to manufacture failure.

## 3. Green: implement the behavior

Make the smallest general implementation that satisfies the agreed behavior.
Run the same tests and the affected existing tests. Do not weaken assertions,
skip tests, special-case fixture values, swallow errors, or mock away the boundary
under test to obtain a pass. Add the next edge or failure case before implementing
its missing behavior. Keep integration evidence for real boundary changes.

Change a test expectation only when requirements or contract evidence shows it
was wrong; explain the correction and re-establish Red for missing behavior.
After code/test failures, make at most two justified repair attempts per cycle,
or honor a stricter project/coordinator limit. Attempts also consume any shared
task repair budget; a new cycle does not reset it. Stop immediately on tooling,
permission, safety, design, or scope blockers and report the smallest next action.

## 4. Refactor and verify the whole change

With tests green, simplify the affected code and test setup without changing
behavior or weakening coverage. Rerun affected tests after refactoring. Repeat
the cycle for remaining criteria; do not add unrelated refactors or speculative
abstractions. A missing required integration run remains a verification gap.

Before delivery, review the full diff for correctness, scope, brittle assertions,
and sensitive data. Run the relevant unit/integration suites and required build,
typecheck, and lint commands. A green exit with skipped or undiscovered required
tests is not completion. Distinguish baseline failures from new failures using
actual evidence. Leave final independent QA to `tp-test` when assigned; TDD does
not by itself prove full acceptance or production readiness.

## Evidence and handoff

Keep a concise record in the current task report or existing coordinator ledger:

- Behavior/criterion and unit/integration test paths; real and mocked boundaries.
- Red command and observed behavioral failure, then Green command and result.
- Final regression/build checks, working directories, executed counts and skips.
- Changed files, unresolved criteria, checks not run, and required approvals.

For tests-only work, hand over the failing assertion and expected outcome to the
implementer. For a blocked run, preserve partial work and state the blocker.
Do not fabricate Red evidence after implementation or claim unexecuted tests pass.
Create a separate report file only when requested or required by project convention.
