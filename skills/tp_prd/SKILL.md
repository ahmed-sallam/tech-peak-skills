---
name: tp_prd
description: Turn the current conversation and relevant codebase context into a short, buildable PRD for ONE feature. Use when the user asks for a PRD, product requirements, a feature spec, or requirements captured before architecture or coding; says "prd", "spec", "اكتب PRD", or "سبيك"; or is ready to hand a discussed feature to a coding agent. Prefer this over a long enterprise-style PRD.
---

# Lean, Buildable PRD

Produce a concise PRD for one feature that a coding agent or the user can implement directly. Synthesize it from what is already known in the conversation and codebase. Treat it as an implementation brief, not a business document.

## Workflow

1. Read the conversation and identify the single feature being requested.
2. Inspect only the relevant area of the repository: related modules, entities, endpoints, tests, and established patterns.
3. Reuse the project's terminology, conventions, and structure.
4. Resolve non-blocking gaps with explicit assumptions. Ask at most one or two questions only when implementation cannot safely proceed without the answer.
5. Write the PRD to `docs/prd/<feature-slug>.md`, creating the directory when needed.

## Rules

- Keep the document roughly to one screen.
- Omit personas, executive summaries, risk matrices, rollout phases, effort estimates, marketing language, and empty sections.
- Make every acceptance criterion observable or testable. Replace vague terms such as "fast", "easy", and "intuitive" with concrete behavior or a justified measurement.
- Name real files, modules, endpoints, and project concepts when the repository provides them. Do not invent parallel abstractions or placeholder paths.
- Match the language of the discussion. Default to English when repository identifiers and documentation are in English.
- Define requirements and implementation touchpoints without expanding into a full architecture document or step-by-step implementation plan.

## Output template

Use this template and omit any section that would be empty:

```markdown
# PRD: <feature name>

**Goal:** <one sentence describing what it does and for whom>

## Why
<2–3 sentences describing the problem and why it matters now>

## Scope

**In:**
- <what will be built>

**Out:**
- <explicit non-goals that prevent scope creep>

## Acceptance criteria

1. <testable, observable, or measurable outcome>
2. <next outcome>

## Technical plan

- **Touchpoints:** <real files, modules, or endpoints to add or change>
- **Data:** <schema or migration changes, or "none">
- **API:** <method, path, and request/response shape, or "none">
- **Key decisions:** <only non-obvious choices, with one line of rationale each>

## Open questions

- <only genuine blockers; omit this section when there are none>
```

## Completion check

- Confirm every acceptance criterion can be checked by reading code, running a test, or using the UI.
- Confirm technical touchpoints refer to repository evidence rather than guesses.
- Confirm the document is concise enough to guide the next architecture or implementation step without another requirements interview.
