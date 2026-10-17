# PAKO'S COMP 441 TRACK C CONTRIBUTION — SEPARATE FROM TEAM REPORT

This package is owned by **Pako** and contains *only* his assigned report sections and proposed CI/CD quality-gate implementation. It does not overwrite Thabiso's, Maano's or Miguel's report documents. It does not claim mutation tests, Django tests or GitHub Actions have already passed.

## Deliverable labels

- **Weeks 5–6 (report methodology):** `docs/pako/WEEK_05_06_Methodology.md`
- **Weeks 7–9 (+Week 11 result update; hybrid rationale):** `docs/pako/WEEK_07_09_Hybrid_Suite_Design_Rationale.md`
- **Week 12 (CI/CD and gates):** `docs/pako/WEEK_12_CICD_Quality_Gate.md`, `docs/pako/quality_gate_policy.json`, `.github/workflows/pako-quality-gate.yml`, `scripts/pako_quality_gate.py`, `tests_pako/test_quality_gate.py`
- **Week 13 (demo):** `docs/pako/WEEK_13_Demo_Checklist.md`
- **Week-by-week status/handoff:** `docs/pako/PAKO_STATUS_AND_HANDOFF.md`
- **Short report-ready Word text (3 pages):** `Pako_Report_Ready_Sections.docx` (the version to send to Thabiso for final report compilation)
- **Expanded editable Word working notes (12 pages):** `Pako_COMP441_Sections.docx` (fuller rationale, tools, and CI notes for your records)

## Safe setup / push

1. Extract this ZIP into the root of https://github.com/keitsengSIR/trackc_group_assignment — the folder with root `manage.py`. **Do not** extract into its nested `hospital-management-system/` directory.
2. Review the new files under `docs/pako` and the additive workflow. No project files are overwritten by these paths in the reviewed repository; check again before copying if teammates have pushed new changes.
3. Test Pako's quality-gate script locally with `python -m unittest discover -s tests_pako -p 'test_*.py' -v`.
4. Push using a separate branch and pull request, following `docs/pako/PAKO_STATUS_AND_HANDOFF.md`.
5. Do not mark Week 12 complete until mutation is measured in the same CI run and the policy has `enforce_mutation=true`.

## Test status (honest)

The five small **quality-gate unit tests** were executed successfully in the authoring environment. They test the gate utility against synthetic XML/JSON, **not** SmartCare healthcare business logic. Django application tests, actual coverage/mutation results, successful GitHub Actions and final BDD/integration test discovery have not been independently verified here.
