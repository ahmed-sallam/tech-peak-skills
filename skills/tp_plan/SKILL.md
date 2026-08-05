---
name: tp_plan
description: Convert an approved PRD and architecture into a concrete, ordered implementation plan for ONE feature. Use after requirements and technical design are settled and before coding, especially when a coding agent needs file-level tasks, dependencies, verification steps, risks, and completion checks without reopening product or architecture decisions.
---

# Implementation Plan

Produce an executable roadmap for one feature. Assume the approved PRD defines what to build and the approved architecture defines how it fits the system. Plan the work without rewriting either artifact or writing code.

## Workflow

1. Read the PRD, architecture document, and relevant codebase areas.
2. Identify dependencies, assumptions, reusable code, and genuine blockers.
3. Order work by dependency and risk. Prefer vertical, independently verifiable increments when the architecture allows them.
4. Break implementation into small steps, each with one clear outcome and its own verification.
5. Name files to create, modify, or remove only when supported by repository evidence. Group changes by module.
6. Include relevant data, backend, API, frontend, integration, testing, documentation, compatibility, and rollback work.
7. Write the result to `docs/plans/<feature-slug>.md`, creating the directory when needed.

## Rules

- Do not change business requirements or redesign the approved architecture.
- Do not write implementation code or estimate time.
- Prefer existing utilities, patterns, and dependencies.
- Make dependencies and ordering explicit.
- Include validation with every step, not only in a final testing section.
- State assumptions and blockers clearly; do not invent filenames or interfaces.
- Include rollback or mitigation steps for schema, public API, authentication, data deletion, CI/CD, and production-impacting changes.

## Output template

```markdown
# Plan: <feature name>

## Summary
<implementation approach and sequencing rationale>

## Inputs
- PRD: <path>
- Architecture: <path>

## Assumptions and dependencies
- <assumption or dependency>

## Implementation steps

### 1. <outcome>
- **Changes:** <specific files, modules, or interfaces>
- **Details:** <what to implement without writing the code>
- **Verify:** <command, test, or observable result>

### 2. <next outcome>
- **Depends on:** <earlier step, if any>
- **Changes:** <specific files, modules, or interfaces>
- **Details:** <what to implement>
- **Verify:** <command, test, or observable result>

## File summary
- **Create:** <paths or "None">
- **Modify:** <paths or "None">
- **Remove:** <paths or "None">

## Risks and mitigations
- **<risk>:** <mitigation>

## Completion checklist
- [ ] Project builds, type-checks, and lints without new errors or warnings.
- [ ] Relevant automated tests pass.
- [ ] Every PRD acceptance criterion is satisfied.
- [ ] Documentation and compatibility notes are updated where required.
- [ ] The final diff is reviewed for regressions, security issues, and leaked secrets.
```
