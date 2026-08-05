# Tech Peak Skills

Lightweight, composable AI coding skills for Claude Code, Kilo Code, and compatible coding agents.

Each skill has a single responsibility and produces an artifact that becomes the input for the next stage of development.

---

# Workflow

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

---

# Skills

## `prd`

Turns the current conversation and codebase into a concise, buildable Product Requirements Document for a single feature.

**Output**

- Problem
- Goals
- Requirements
- User stories
- Acceptance criteria
- Scope
- Assumptions

Install

```bash
npx skills add https://github.com/ahmed-sallam/tech-peak-skills --skill prd
```

---

## `architecture`

Transforms an approved PRD into a technical design that fits the existing codebase.

**Output**

- Architecture decisions
- Domain model
- Database changes
- API design
- Frontend structure
- Integration points
- Risks
- Trade-offs

Install

```bash
npx skills add https://github.com/ahmed-sallam/tech-peak-skills --skill architecture
```

---

## `plan`

Creates an ordered implementation roadmap from the architecture and PRD.

**Output**

- Implementation steps
- File changes
- Migration order
- Testing strategy
- Validation checklist
- Execution sequence

Install

```bash
npx skills add https://github.com/ahmed-sallam/tech-peak-skills --skill plan
```

---

# Install All Skills

```bash
npx skills add https://github.com/ahmed-sallam/tech-peak-skills
```

---

# Manual Installation

Copy the desired skill into either:

Project-specific

```text
.claude/skills/<skill-name>/SKILL.md
```

or globally

```text
~/.claude/skills/<skill-name>/SKILL.md
```

Examples

```text
.claude/skills/prd/SKILL.md
.claude/skills/architecture/SKILL.md
.claude/skills/plan/SKILL.md
```

---

# Philosophy

Each skill should have one responsibility.

| Skill | Responsibility |
|--------|----------------|
| **PRD** | Decide **what** should be built |
| **Architecture** | Decide **how it fits** into the existing system |
| **Plan** | Decide **how to implement** the feature |
| **Implementation** | Write the code |
| **Review** | Validate correctness and quality |

Keeping these concerns separate produces more consistent outputs and allows different AI agents to specialize in each stage.
