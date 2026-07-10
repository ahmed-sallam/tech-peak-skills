# tech-peak-skills
 
Agent skills for Claude Code / Kilo Code.
 
## Skills
 
- **`prd`** — turns the current conversation + codebase into a short, buildable PRD
  for one feature. No interview, no fluff; outputs to `docs/prd/<feature>.md`.
## Install
 
```bash
npx skills add https://github.com/ahmed-sallam/tech-peak-skills --skill prd
```
 
Or copy `skills/prd/SKILL.md` into `.claude/skills/prd/SKILL.md` (per project)
or `~/.claude/skills/prd/SKILL.md` (global).
 
