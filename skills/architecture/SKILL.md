---
name: architecture
description: Convert an approved PRD into an implementation architecture for the existing codebase. Analyze where the feature belongs, what should change, what should remain unchanged, and identify architectural risks before coding. Use this before creating an implementation plan.
---

# Architecture Design

Produce a concise technical design for ONE feature.

The output should describe HOW the feature should fit into the current system.

This is NOT an implementation plan.

This is NOT a PRD.

Assume the PRD already exists.

---

## Goals

- Fit naturally into the existing architecture.
- Reuse existing code whenever possible.
- Minimize coupling.
- Keep the design simple.
- Avoid unnecessary abstractions.
- Preserve existing conventions.
- Prefer consistency over novelty.

---

## Review Process

### 1. Understand the Existing Architecture

Analyze:

- modules
- packages
- services
- boundaries
- naming conventions
- dependency direction
- existing APIs
- database model
- security model

Reuse existing patterns whenever reasonable.

---

### 2. Define Feature Placement

Explain:

- where the feature belongs
- why it belongs there
- what existing components should be reused
- what new components are necessary

Avoid creating new services or layers unless clearly justified.

---

### 3. Domain Design

Identify:

- aggregates
- entities
- value objects
- repositories
- services
- events

Only introduce new domain concepts if required.

---

### 4. Data Model

Describe:

- new tables
- modified tables
- indexes
- constraints
- migrations

Explain why each change is needed.

---

### 5. API Design

Describe:

- endpoints
- DTOs
- validation
- authorization
- pagination
- filtering
- error handling

Do not write implementation code.

---

### 6. Frontend Design

Describe:

- pages
- components
- routes
- forms
- state management
- caching
- permissions

Reuse existing UI patterns.

---

### 7. Integration Points

Identify:

- RabbitMQ
- Redis
- external APIs
- scheduled jobs
- file storage
- notifications
- audit logging

Only include integrations that are actually needed.

---

### 8. Non-Functional Considerations

Evaluate:

- security
- scalability
- maintainability
- observability
- performance
- concurrency
- reliability

Highlight anything unusual.

---

### 9. Risks

Identify:

- architectural risks
- technical debt
- migration risks
- backward compatibility
- operational risks

For each risk:

- explain it
- estimate severity
- propose mitigation

---

### 10. Alternatives

If there are multiple reasonable designs:

Explain:

- Option A
- Option B

Include trade-offs.

Recommend one.

---

## Output Format

# Summary

A short description.

# Current Architecture

...

# Proposed Design

...

# Data Model

...

# API

...

# Frontend

...

# Integrations

...

# Non-Functional Considerations

...

# Risks

...

# Alternatives

...

# Recommendation

...

---

## Rules

- Do not write code.
- Do not create implementation tasks.
- Do not estimate time.
- Do not invent business requirements.
- Stay aligned with the PRD.
- Prefer modifying existing code over introducing new abstractions.
- Clearly state assumptions.
