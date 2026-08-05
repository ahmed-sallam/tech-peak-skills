---
name: tp_architecture
description: Convert an approved PRD into a concise implementation architecture for ONE feature in an existing codebase. Use before implementation planning when a feature is architectural, cross-cutting, security-sensitive, data-model-sensitive, or needs explicit decisions about placement, boundaries, APIs, integrations, and risks.
---

# Feature Architecture

Design how one approved feature should fit the current system. Produce technical decisions and boundaries, not product requirements, implementation tasks, estimates, or code.

## Workflow

1. Read the approved PRD and identify its constraints and acceptance criteria.
2. Inspect the relevant modules, boundaries, dependencies, data model, APIs, security model, tests, and naming conventions.
3. Identify existing components and patterns to reuse before proposing new ones.
4. Define the feature's placement, responsibilities, interfaces, data flow, and dependency direction.
5. Evaluate data, API, frontend, integration, security, reliability, performance, observability, concurrency, and backward-compatibility impacts only where relevant.
6. Compare viable alternatives when a consequential trade-off cannot be resolved by repository evidence. Recommend one and explain why.
7. Write the result to `docs/architecture/<feature-slug>.md`, creating the directory when needed.

## Rules

- Stay within the approved PRD; do not invent or change business requirements.
- Prefer existing conventions and components over new services, layers, or abstractions.
- Introduce domain concepts, storage, integrations, and infrastructure only when the feature requires them.
- State assumptions and cite repository evidence for important decisions.
- For each material risk, state severity, impact, and mitigation.
- Do not write code, create implementation tasks, or estimate time.

## Output template

```markdown
# Architecture: <feature name>

## Summary
<proposed design in a short paragraph>

## Current architecture
<relevant boundaries, components, patterns, and constraints>

## Proposed design
<placement, responsibilities, interfaces, data flow, and reused components>

## Data model
<tables, fields, indexes, constraints, migrations, or "No change">

## API and contracts
<endpoints, events, DTOs, validation, authorization, errors, or "No change">

## Frontend
<routes, components, state, caching, permissions, or "Not applicable">

## Integrations
<external systems, queues, jobs, storage, notifications, or "None">

## Non-functional considerations
<security, reliability, performance, observability, concurrency, and compatibility>

## Risks and mitigations
- **<severity> — <risk>:** <impact and mitigation>

## Alternatives
<viable alternatives and trade-offs; omit when there is only one reasonable design>

## Recommendation
<chosen design and concise rationale>
```
