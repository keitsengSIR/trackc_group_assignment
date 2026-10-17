# PAKO | COMP 441 Track C | Hybrid Suite Design Rationale (Weeks 7–9, updated Week 11)

**Owner:** Pako  
**Project:** SmartCare patient/appointment modules  
**Status (17 October 2026):** Source-grounded rationale drafted; the mutation-survivor IDs, passing test names, coverage and mutation scores must come from actual reports.

## Draft report text

A hybrid test suite combines AI-assisted test drafts with manually designed unit tests, integration tests and acceptance tests. AI is efficient for generating examples and parameterized cases, but its output may encode invented field constraints, exercise helper functions rather than application logic, or make assertions too weak to detect wrong behaviour. Human-authored tests therefore address the failure modes indicated by line/branch coverage, surviving mutants and domain risks. In SmartCare this is especially important for patient identifiers, record dates, doctor availability, appointment conflicts and role-based access. A test is included for a traceable reason—an uncovered business requirement, a missed decision branch, or a surviving mutation—not merely to increase test counts.

### How tests are designed in this repository

| Target and source | Named design technique | Proposed meaningful assertion (not yet claimed as executed) | Why AI-only tests may miss it | Evidence owner |
|---|---|---|---|---|
| Patient DOB and calculated `age`, `patient/models.py` | Boundary value analysis | Correct age on birthday, day before birthday and around leap-day birthdays; no arbitrary upper bound unless requirements establish one | Existing `test_patient_validation.py` tests its own toy `validate_patient_age`, not production code | Maano / Miguel |
| Patient registration required contact and identity fields, `patient/forms/patients.py` | Equivalence partitioning | Form accepts valid required fields and rejects blank/malformed values; no real PII in fixtures | AI may invent an `age` form field or medical ID format | Miguel |
| Auto-generated `patient_id`, `patient/models.py` | State transition + uniqueness/concurrency | Two distinct patient records have distinct generated IDs; record id remains stable on update | Sequence/count logic can pass a single-record happy path but fail after deletions or concurrent inserts | Miguel |
| Appointment start/end times, `appointment/models.py` | Boundary value analysis | Start == end rejected, start > end rejected, adjacent nonoverlap accepted | Strict vs non-strict comparison mutants may survive | Miguel |
| Appointment overlap with same doctor/patient, `appointment/models.py` | Decision table | Overlapping appointments rejected, nonoverlapping accepted, different doctor/patient distinguished | Single happy-path appointment does not exercise decision combinations | Miguel |
| Doctor availability and emergency flow, `appointment/models.py` | Decision table | Regular outside hours rejected; emergency exemption tested subject to actual application rules | AI may assume that emergency skips every check; the code still checks overlap | Miguel |
| Approved doctor leave, `appointment/models.py` | State transition testing | Non-emergency conflict rejected when leave approved; examine pending/rejected states separately | AI may never set up leave/appointment data together | Miguel |
| Medical record–patient relation, `patient/models.py` | Integration + referential integrity | Record associates with saved patient; properly configured patient deletion and record constraints behave consistently | Mocks do not exercise SQLite relationships | Miguel |
| Receptionist/doctor/nurse permissions, `users/middleware.py`, `core/decorators.py` | Decision table | Allowed role accesses a relevant view; unauthorised role blocked without exposing patient details | AI may assert only a response code or omit authorization | Miguel |
| Updates to registration data, `patient/models.py` | State transitions | Persist, reload, update and delete appropriate synthetic record; verify fields and count changes | Weak `assert True` tests prove nothing | Miguel |

**Important discovered weak assertions:** `test_integration.py` currently ends with `assert True` and does not persist a patient. `test_patient_validation.py` defines the tested validation function inside the test module. Neither establishes tested production patient registration constraints. Avoid counting those assertions as independent confirmation of the application.

### Traceability from manual tests to the mutation report

After Maano's AI-only mutation v1, every manual test should have one row in the evidence log below. The tests, mutant identifiers and actual outcomes must be populated by the authors who ran them.

| v1 mutant ID + location | Surviving change | New manual test ID/file | Technique | v2 outcome | Owner |
|---|---|---|---|---|---|
| [Maano to supply] | [actual diff] | [test path::test name] | [named technique] | [killed / survived] | Maano + Miguel |
| [Maano to supply] | [actual diff] | [test path::test name] | [named technique] | [killed / survived] | Maano + Miguel |
| [Maano to supply] | [actual diff] | [test path::test name] | [named technique] | [killed / survived] | Maano + Miguel |

The assignment requires **at least eight** v1 surviving-mutant root-cause analyses and specific manual tests. Pako documents the design reasoning but should not invent survivor IDs, test failures or scores. Maano supplies the actual eight or more mutant records; Miguel links automated Django/BDD tests. Thabiso maintains RTM mappings.

### Risk-led test execution priority (proposed, pending Maano's ranked list)

1. Patient identity/record changes and authorization: highest privacy and data-integrity risk.
2. Appointment conflict, emergency and leave rules: high patient-safety and scheduling impact.
3. Django ORM integration and role-based route access: detects component interface faults missed by mocks.
4. Medication/stock and billing calculations: important cross-module consistency risks when included in scope.
5. UI display-only and reporting formatting: generally lower immediate data-integrity impact.

This is a *draft rationale*, not the final AI-guided ranking; Maano must provide the assigned test-execution order and justify it using actual churn/complexity/mutation data or a transparent risk heuristic.

### Comparing AI-only and hybrid suites fairly

Keep the target functions, mutation-tool version, test environment and excluded mutants unchanged. Preserve AI-generated files separately so `AI-only` genuinely excludes manually added tests. Report statement and branch coverage separately and calculate the mutation delta as `(v2 score – v1 score)` percentage points. Report genuine trade-offs: hybrid testing is slower to design and maintain, but precise assertions and integration coverage may expose errors missed by AI-produced examples. Do not assert improvement until v2 is measured.

### Source notes

Repository `patient/models.py`, `patient/forms/patients.py`, `appointment/models.py`, `test_patient_validation.py`, `test_integration.py`, `users/middleware.py` and `core/decorators.py`, alongside brief Sections 7.4–7.6. Source reviewed 17 October 2026.
