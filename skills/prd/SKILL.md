---
name: prd
description: Turn the current conversation and codebase into a short, buildable PRD for ONE feature — no interview, no fluff. Use this whenever the user asks to write a PRD, a spec, or to plan out a feature; wants requirements written down before coding; says "prd" / "spec" / "اكتب PRD" / "سبيك"; or has just finished discussing a feature and is ready to hand it to a coding agent. Always prefer this over writing a long enterprise-style PRD.
---

# PRD (lean, buildable)

Produce a one-screen PRD that a coding agent — or the user — can implement directly.
Synthesize it from what is already known: the conversation and the codebase.
This is an implementation brief, not a business document.

## Core rules

- **Don't interview.** Build the PRD from the conversation + repo. Ask at most 1–2
  questions and only if something is a genuine blocker. Otherwise state your
  assumption inline under the section it affects and move on.
- **Read before writing.** Skim only the feature's area of the repo — the relevant
  modules, entities, endpoints, and existing patterns. Reuse the project's own names,
  conventions, and structure; do not invent parallel ones.
- **Cut everything cuttable.** No personas, no executive summary, no risk matrix, no
  rollout phases, no effort estimates, no marketing. If a section has nothing real to
  say, delete it.
- **Make every criterion testable.** Replace vague words ("fast", "easy", "intuitive")
  with observable behavior or numbers ("validation error shows on empty email",
  "list loads in < 300ms").
- **Match the language** of the discussion. Default to English when the codebase's
  identifiers and docs are in English.

## Output

Write the PRD to `docs/prd/<feature-slug>.md` (create the folder if needed).
Use exactly this template, omitting any section that would be empty:

```markdown
# PRD: <feature name>

**Goal:** <one sentence — what it does and for whom>

## Why
<2–3 sentences: the problem and why now>

## Scope
**In:**
- <what we build>

**Out:**
- <explicit non-goals, to stop scope creep>

## Acceptance criteria
1. <testable / observable / measurable>
2. ...

## Technical plan
- **Touchpoints:** <real files / modules / endpoints to add or change>
- **Data:** <schema or migration changes, or "none">
- **API:** <method + path + request/response shape, or "none">
- **Key decisions:** <only non-obvious choices, one line of rationale each>

## Open questions
- <only real blockers — delete this whole section if there are none>
```

## Definition of done

- Fits on roughly one screen. If it is longer, you are adding bloat — trim it.
- Every acceptance criterion is checkable by reading code or clicking the UI.
- The technical plan names real paths and modules from the repo, not placeholders.
- Someone could start coding from it without asking you a follow-up question.
