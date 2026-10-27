# | COMP 441 Track C | Methodology (Weeks 5–6; update through Week 12)

**Owner:** Pako  
**Project:** SmartCare hospital management system  
**Repository:** https://github.com/keitsengSIR/trackc_group_assignment  
**Status (17 October 2026):** Drafted from repository source; execution metrics and local tool versions remain unverified.

## Methodology for the final group report (Pako's section)

This project applies a risk-based, multi-level verification strategy to the existing SmartCare Django application. The software contains patient registration and medical records, doctor availability and appointments, role-based workflows, and pharmacy/billing features. Testing targets patient privacy and clinical-record integrity first, because errors in these areas can lead to incorrect registration, double-booking, unauthorised access or misleading records. The sequence mandated by the brief is: establish repository and static-analysis baseline; generate an **AI-only** unit-test baseline; measure statement/branch coverage; run first mutation test; add manually designed tests targeting surviving mutants; apply TDD/BDD and integration testing; repeat mutation testing; and finally enforce verified quality metrics in CI. The comparison must use consistent mutation scope, tools, and exclusions.

### Source-verified versus proposed tools

| Tool/component | Purpose | Version/evidence | Current state |
|---|---|---|---|
| Python | Application language and test runner | Version not pinned in repository; **3.11 proposed for CI** | CI runtime choice, not a verified developer-local version |
| Django | Application/web framework and Django test models | **django==4.2.9** in root `requirements.txt` | Source verified |
| SQLite | Transactional test DB / Django ORM integration | Configured in `hms_project/settings/base.py`; SQLite engine version not checked | Source verified |
| Pytest | Parametrized/AI/manual unit test execution | `test_patient_validation.py` imports pytest; version not pinned by repository | Existing use; version to record with `pytest --version` |
| pytest-django | Django DB fixtures and integration testing | Not in root `requirements.txt`; proposed >=4.8,<5 | Pending installation/verification |
| pytest-cov / coverage.py | Statement and branch coverage + XML | Not in root `requirements.txt`; proposed >=5,<8 | Pending execution |
| mutmut | Python mutation analysis (v1 and v2) | No pinned root dependency; suggested in assignment | **Mutation owner: Maano; tool/version and report pending** |
| Pylint | Static code analysis | Referenced in `Reports/Quality_Track_C_Report.md` | Output belongs to Miguel; capture `pylint --version` |
| scikit-learn | Track C defect/churn risk model | Imported in `train_defect_classifier.py`; no pinned root dependency | Miguel's specialist stream; validation of defect labels needed |
| Git / GitHub | Version control, peer reviews, commit evidence | Public GitHub repository; versions unverified | Source verified |
| GitHub Actions | Automated verification | No `.github/workflows/` in public repository at review time | Pako's **new proposed** workflow |
| ChatGPT or other LLM | Draft AI test cases and suggested scenarios | Confirm actual model and date from Maano's prompt log | Unverified; do not claim usage by the group |

**Version-capture commands before submitting the report:** `python --version`, `python -m django --version`, `python -m pytest --version`, `python -m pip show pytest-django pytest-cov coverage mutmut pylint scikit-learn`, `git --version`, plus the CI run's Python setup line. Document the date and commit SHA with each measurement.

### Environment and scope

Repository root refers to the folder containing **root-level `manage.py`**, `patient/`, `appointment/`, `hms_project/`, and `requirements.txt`. The GitHub repository also contains a **nested `hospital-management-system/` copy**; do not run measurement twice or mix modules from the two copies. `hms_project/settings/base.py` configures SQLite; `hms_project/settings/dev.py` selects development settings and is appropriate for an isolated CI test database (never use real patient data). Set `DJANGO_ENV=dev`, `DJANGO_SETTINGS_MODULE=hms_project.settings.dev`, a synthetic `SECRET_KEY`, and an in-memory email backend in CI.

### Test levels, measurement, and controls

1. **Static baseline (Miguel):** run linter/complexity tooling, triage severity and compare LLM suggestions to actual code behavior. A symbolic-execution discussion is required by the brief but is not equivalent to executed symbolic analysis.
2. **AI-only unit baseline (Maano):** retain prompt text and AI-generated test files separately. Record exact executable tests, meaningful assertions, baseline line/branch coverage, and mutation v1. Do not mix manual repairs into the AI-only baseline.
3. **Human-designed hybrid (Maano/Miguel; documented by Pako):** select cases by equivalence partitions, boundary analysis, decision tables and state transitions, then link each test to a surviving mutant or uncovered branch; the source code, assertions and traceability records must agree.
4. **Integration and acceptance (Miguel):** test real Django ORM + SQLite, patient registration flow, doctor availability, appointments, permissions and key business paths; automate at least three Gherkin scenarios and at least five distinct integration tests.
5. **Track C specialist (Miguel):** derive churn/commit features and test a defect-risk model. **Important validity note:** current `train_defect_classifier.py` sets `is_defective` from above-median `total_lines_changed`, then uses that same feature as input. High measured model accuracy cannot be presented as independently verified defect prediction. Obtain defect labels from real fixed-bug history or describe honestly as churn-risk classification.
6. **Final comparison and quality gate (Maano + Pako):** run both AI-only and hybrid suites against a common, disclosed mutation scope; rerun after manual tests. Upload coverage and mutation evidence from the tested commit. Enforce the group-approved thresholds in GitHub Actions on push/pull request.

### Measurement conventions

- Line coverage: executed lines / measured executable lines × 100 (from same-run `coverage.xml`). Branch coverage: covered branches / total branches × 100, reported separately.
- Mutation score: killed mutants / (killed + surviving mutants) × 100; record timeout/error/equivalent mutant treatment explicitly and apply the same policy to v1 and v2.
- RTM completeness: requirements with ≥1 passing mapped test / total requirements × 100 (Thabiso's RTM).
- Defect density: confirmed new defects found during this project / application KLOC in measured scope (Miguel/Maano findings).
- Do not report 100% results from the current heuristic churn classifier as a validated defect model.

### Reproducibility and ethics

Use synthetic patient fixtures and Django's ephemeral test database. Never push `.env` secrets, SMTP passwords, private patient records, or full personal data into CI logs or Git. Require traceable commits, exact tool versions, immutable `GITHUB_SHA`, and actual CI logs before marking a step completed. Any AI-generated tests must be reviewed by the group and declared in the one-page AI-use declaration.

### Source notes

- Assignment brief: Sections 7.3–7.10, particularly 7.4–7.6 and 7.10 (provided COMP 441 PDF).
- Repository: `README.md`; `requirements.txt`; `hms_project/settings/base.py`; `hms_project/settings/dev.py`; `patient/models.py`; `patient/forms/patients.py`; `appointment/models.py`; `test_patient_validation.py`; `test_integration.py`; `train_defect_classifier.py`; `Reports/Quality_Track_C_Report.md` (public default branch reviewed 17 Oct 2026).

**Before final submission:** Add actual package versions, tested commit SHA, locations of Maano/Miguel's evidence, final project constraints/exclusions, and measured baseline/results. This draft is not a claim that tests have executed successfully.
