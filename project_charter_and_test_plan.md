# COMP 441 Project Charter & Test Plan — Track C (Healthcare System)

## 1. Project Charter & Group Roles
* **Test Lead / Coordinator**: Manages overall test strategy, milestone tracking, and weekly stand-ups.
* **Automation & CI/CD Engineer**: Sets up the test runner, fixtures, and GitHub Actions CI pipeline with quality gates.
* **AI Test Engineer**: Manages AI prompt engineering, baseline test generation, and mutation benchmarking.
* **Quality & Specialist Track Officer (Track C)**: Owns the scikit-learn defect-prediction classifier and healthcare data validation rules.
* **Documentation & Report Lead**: Maintains logs, traceability matrices, and compiles the final report.

### Track C Justification (Half-Page Summary)
Our group selected an open-source clinic and patient-appointment management system. Healthcare software requires stringent data validation (patient IDs, dates of birth, consultation schedules, and encrypted health records) to ensure patient safety and data privacy. Testing a healthcare domain allows us to rigorously evaluate how AI-generated test suites handle strict boundary value constraints, equivalence partitioning on sensitive inputs, and defect-prediction modeling based on historical code churn.

---

## 2. IEEE-829 Test Plan
* **Scope**: Validates patient intake forms, appointment scheduling modules, and data-validation utility libraries within the clinic system.
* **Objectives**: Achieve >85% statement coverage, >70% mutation score on the hybrid suite, and zero unhandled data-validation exceptions.
* **Methodology**: Hybrid testing combining AI-generated baseline tests, manual test-case design (boundary value analysis and equivalence partitioning), property-based testing, and mutation testing (`mutmut`).
* **Schedule**: Phased weekly milestones from Week 5 (Charter/Setup) to Week 12 (Final Hybrid Suite & CI/CD).
* **Entry / Exit Criteria**:
  * *Entry*: Repository cloned, dependencies installed, local test runner passing.
  * *Exit*: All critical defects resolved, mutation score improved from v1 to v2, CI quality gate passing.

---

## 3. Risk Register
| Risk ID | Description | Probability (1-5) | Impact (1-5) | Risk Score | Mitigation Strategy |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **R1** | AI-generated tests contain loose assertions (`assertTrue(True)`). | 4 | 4 | 16 | Manual review of all AI test assertions; strict mutation testing (v1). |
| **R2** | Mutation testing tool (`mutmut`) takes too long to run on large modules. | 3 | 4 | 12 | Scope testing down to core patient-validation and appointment sub-packages. |
| **R3** | Missing test fixtures or database connection errors in CI environment. | 3 | 3 | 9 | Use in-memory SQLite databases and mock fixtures for unit/integration tests. |
| **R4** | Team schedule conflict during integration testing phase. | 2 | 4 | 8 | Weekly stand-ups and modular task delegation by role. |
| **R5** | Over-reliance on AI co-pilot code suggestions leading to logic flaws. | 3 | 3 | 9 | Mandatory peer code reviews and strict TDD red-green-refactor logs. |

---

## 4. Effort Estimation (Three-Point Estimation)
Using **Three-Point Estimation** ($E = \frac{O + 4M + P}{6}$):
* **Phase 1 (AI Baseline & Mutation v1)**: Optimistic ($O$) = 4 hours, Most Likely ($M$) = 7 hours, Pessimistic ($P$) = 10 hours $\rightarrow$ **Estimated = 7 hours**.
* **Phase 2 (Manual Gap-Closing & Hybrid Suite v2)**: Optimistic ($O$) = 8 hours, Most Likely ($M$) = 12 hours, Pessimistic ($P$) = 22 hours $\rightarrow$ **Estimated = 13 hours**.