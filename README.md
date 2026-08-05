# Tech Peak Skills

Lean, composable agent skills for turning one feature idea into implementation-ready guidance. Each skill owns one stage, produces one artifact, and hands that artifact to the next stage.

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
Review
  ↓
Pull Request
```

This repository currently provides the three planning skills in that workflow:

| Skill | Question it answers | Default artifact |
| --- | --- | --- |
| `tp_prd` | What should we build? | `docs/prd/<feature-slug>.md` |
| `tp_architecture` | How should it fit the existing system? | `docs/architecture/<feature-slug>.md` |
| `tp_plan` | In what order should we implement it? | `docs/plans/<feature-slug>.md` |

Implementation, review, and pull-request creation remain execution stages rather than packaged skills in this repository.

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

## Naming and migration

All Tech Peak skills use the `tp_` namespace to avoid collisions with similarly named built-in or community skills.

| Previous name | Current name |
| --- | --- |
| `prd` | `tp_prd` |
| `architecture` | `tp_architecture` |
| `tp_plan` | `tp_plan` |

If you installed an earlier version manually, remove the old `prd` and `architecture` skill folders after installing their renamed replacements.

## Design principles

- Give every skill one responsibility and one primary artifact.
- Use repository context and existing conventions instead of inventing parallel structures.
- Keep requirements, architecture, planning, implementation, and review separate.
- Prefer concise, testable, implementation-ready outputs.
- State assumptions when missing information is not a genuine blocker.
