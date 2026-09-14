# Backend and business invariants

Choose only cases relevant to the stated behavior. Use actual test framework and
database conventions from the project; the tools below are mappings, not mandatory
dependencies or instructions to install them.

- JUnit/Mockito: deterministic rules and boundaries; mock collaborators, not the
  calculation or rule being verified. Assert externally meaningful results.
- Spring Boot Test/Testcontainers: persistence, constraints, transactions, and
  database-specific behavior. Check the configured database engine/version and
  disposable target. Container startup may download an image or run schema setup;
  verify permission before execution. Do not substitute an in-memory database when
  its behavior cannot prove the relevant SQL or transaction semantics.
- Existing MockMvc/REST Assured/equivalent: validation, response shape/status,
  authenticated and unauthenticated access, role/tenant isolation, and durable effects.
  Reuse the established harness instead of adding another API testing library.
- ArchUnit/equivalent: enforce documented or existing module/layer rules. A new
  architecture decision requires confirmation; a QA pass does not establish policy.
- Existing static analysis: run relevant configured checks; never disable a rule
  or suppress warnings just to obtain a clean result.

## Cross-module transaction example

For a synthetic fee payment, map each actual acceptance criterion to evidence:

| Property, if required by the feature | Evidence |
| --- | --- |
| Valid amount, precision, rounding, remaining balance | Unit boundary cases against the documented rules |
| Payment, balance, journal, and audit stay consistent | Integration assertions on persisted state |
| Failure halfway through the operation | No forbidden partial commit; assert the documented transaction boundary |
| Duplicate submission or retry | Assert the specified idempotency/duplicate handling, without inventing it |
| Simultaneous updates | Deterministic integration test of the required concurrency behavior |
| Wrong role or tenant | API denial and unchanged protected state |
| Receipt and refreshed balance visible to the user | Targeted browser journey against the isolated backend |

Do not assume accounting signs, rounding policy, permissions, or duplicate handling
from the current implementation. Resolve unclear requirements before declaring a defect.

Avoid tests whose enclosing rollback transaction hides application commit behavior.
Verify outcomes across the appropriate transaction boundary when that is the risk.
Use controlled synchronization for concurrency tests rather than sleep-based races;
never stress a shared environment as a substitute for a deterministic case.

Contract/property testing with an existing OpenAPI/Schemathesis setup can be useful
for a changed contract. Read its target and mutation scope first. Security tools
such as ZAP and load/fuzz workloads require an explicitly authorized scope and safe
target; normal API negative tests do not authorize a full audit or active scan.
