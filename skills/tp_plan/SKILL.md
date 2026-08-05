---
name: tp_plan
description: Convert an approved PRD and architecture into a concrete implementation plan. Produce an ordered, buildable roadmap for ONE feature before coding. Focus on execution, not requirements or design.
---

# Implementation Plan

Produce a concise implementation plan for ONE feature.

Assume the PRD has already been written.

Assume the architecture has already been decided.

This skill answers:

> "How should we implement this feature?"

It is NOT a PRD.

It is NOT an architecture document.

It is NOT a code review.

It is NOT an implementation.

---

## Goals

- Produce an implementation roadmap.
- Minimize unnecessary work.
- Reuse existing code whenever possible.
- Break work into small, verifiable steps.
- Reduce implementation risk.
- Keep tasks independently testable.

---

## Planning Process

### 1. Review Inputs

Read:

- PRD
- Architecture document
- Existing codebase

Identify:

- dependencies
- assumptions
- reusable code
- blockers

---

### 2. Define Implementation Order

Arrange work in the safest order.

Typical order:

1. Domain
2. Database
3. Backend
4. API
5. Frontend
6. Integration
7. Tests
8. Documentation

Reorder if another sequence reduces risk.

---

### 3. Identify File Changes

List files likely to:

- create
- modify
- remove (rare)

Group them by module.

Do not invent filenames if unknown.

---

### 4. Database Work

Describe:

- migrations
- indexes
- constraints
- seed data
- rollback considerations

---

### 5. Backend Tasks

Describe:

- services
- repositories
- controllers
- DTOs
- validation
- authorization
- events

---

### 6. Frontend Tasks

Describe:

- pages
- routes
- components
- forms
- state management
- caching
- permissions

---

### 7. Testing Strategy

Include:

- unit tests
- integration tests
- API tests
- UI tests (if applicable)
- manual validation

---

### 8. Risks

Identify implementation risks.

For each risk:

- explain
- mitigation

---

### 9. Validation Checklist

Before considering the feature complete:

- Builds successfully
- Tests pass
- Acceptance criteria satisfied
- No obvious regressions
- Documentation updated

---

# Output Format

## Summary

Short overview.

## Assumptions

...

## Dependencies

...

## Implementation Steps

### Step 1

...

### Step 2

...

### Step N

...

## File Changes

...

## Database

...

## Backend

...

## Frontend

...

## Testing

...

## Risks

...

## Completion Checklist

- [ ]

- [ ]

- [ ]

---

## Rules

- Do not write code.
- Do not redesign the architecture.
- Do not change business requirements.
- Keep steps small and sequential.
- Prefer modifying existing code over introducing new abstractions.
- State assumptions explicitly.
- Keep the plan implementation-focused.
