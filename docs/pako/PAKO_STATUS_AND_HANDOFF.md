**Project:** COMP 441, Track C, SmartCare  
**Owner:** Pako 
**Prepared:** 17 October 2026  
**Repository:** https://github.com/keitsengSIR/trackc_group_assignment

## Status by brief week

| Week | Pako's work | File(s) | Exact status at handoff |
|---|---|---|---|
| 5 (15 Sep) | Test automation tooling choices input to charter | `WEEK_05_06_Methodology.md` | **Drafted**; tool versions for local runs remain unverified |
| 6 (22 Sep) | Methods/toolchain and AI-vs-manual measurement method | `WEEK_05_06_Methodology.md` | **Drafted**; Maano's AI-only baseline pending |
| 7 (06 Oct) | Explain design rationale for mutation-survivor manual tests | `WEEK_07_09_Hybrid_Suite_Design_Rationale.md` | **Drafted**; needs actual v1 survivor links |
| 8 (13 Oct) | TDD/BDD test-level design coordination | `WEEK_07_09_Hybrid_Suite_Design_Rationale.md` | **Coordination described**; Miguel owns execution/evidence |
| 9 (20 Oct) | Hybrid suite rationale final linkage | `WEEK_07_09_Hybrid_Suite_Design_Rationale.md` | **Drafted**; named passing test IDs and RTM mappings pending |
| 10 (27 Oct) | Metrics and specialist tooling method note | Methodology document | **Drafted**, not specialist classifier owner's work |
| 11 (03 Nov) | Incorporate v2 mutation result into rationale/gate | Hybrid rationale + gate policy | **Pending** Maano's actual v2 results |
| 12 (10 Nov) | CI pipeline source files and quality-gate justification | `.github/workflows/pako-quality-gate.yml`, `scripts/pako_quality_gate.py`, `docs/pako/quality_gate_policy.json`, `WEEK_12_CICD_Quality_Gate.md` | **Initial source prepared; self-tests pass; final mutation enforcement and CI passing run pending** |
| 13 (17 Nov) | Live passing/failing CI quality-gate demonstration | `WEEK_13_Demo_Checklist.md` | **Planned**, no run claimed |

## Handoff boundaries / do not edit teammates' work

- **Thabiso:** executive summary, charter/risk overview, RTM, reflection, appendices. Send Thabiso final confirmed methodology, thresholds, run URLs, and the source file path. Do not rewrite their RTM.
- **Maano:** AI-only coverage, v1 and v2 mutation evidence, survivor list, exploratory session. Ask for original machine-readable evidence and actual commit SHA. Do not invent mutant IDs.
- **Miguel:** static/symbolic analysis, TDD/BDD, integration/acceptance tests, Track C classifier and performance/usability. Ask for real test filenames and their commands to update CI. Do not claim unrun tests passed.
- **Pako:** methodology tools/versions, hybrid test-design explanation, CI implementation/quality-gate justification.

## Files to copy when pushing your contribution

Copy the ZIP's folders **into the root of the repository containing root `manage.py`**. Preserve paths. The workflow filename is intentionally distinct, so it will not overwrite a teammate's current or future `trackc-tests.yml`. If the team uses one unified workflow, merge the *steps* rather than keeping two expensive, conflicting CI pipelines.

```bash
git checkout -b docs/pako-methodology-ci
# Copy docs/pako, scripts/pako_quality_gate.py, tests_pako/test_quality_gate.py,
# and .github/workflows/pako-quality-gate.yml from the ZIP into repository root.
git add docs/pako scripts/pako_quality_gate.py tests_pako/test_quality_gate.py .github/workflows/pako-quality-gate.yml
git commit -m "docs(ci): add Pako methodology, hybrid rationale and provisional quality gate"
git push -u origin docs/pako-methodology-ci
```

Open a pull request rather than pushing directly to `main`; request one member to review coverage thresholds, mutation integration and test discovery. A pull request title could be **`Pako: methodology, hybrid rationale, and Week 12 CI quality-gate draft`**.

## Completion requirements before Pako marks Week 12 DONE

1. Run actual unit/integration/acceptance tests; record each level's command.
2. Collect current-run `coverage.xml` and record its real line/branch rates.
3. Integrate mutmut current-run evidence from Maano, enable `enforce_mutation` and enforce *both* group-approved thresholds.
4. Save passing and intentionally failing GitHub Actions URLs/screenshots.
5. Update these markdown files and the Word file with the actual data; then send the final excerpts to Thabiso.
6. Coordinate the one-page AI tool use declaration with group documentation lead.
