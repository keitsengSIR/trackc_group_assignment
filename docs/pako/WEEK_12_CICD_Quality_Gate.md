# PAKO | COMP 441 Track C | CI/CD Pipeline Summary and Quality-Gate Justification

**Relevant delivery:** Week 12 (10 November 2026) final submission, Week 13 (17 November 2026) live demonstration.  
**Owner:** Pako  
**Status (17 October 2026):** Initial pipeline drafted; gate is **not yet final**. No successful GitHub Actions run is claimed.

## Final report section: CI/CD methodology and justification

The proposed pipeline uses GitHub Actions to run on each push and pull request against the root SmartCare Django project. It installs the application dependencies plus Pytest, pytest-django and pytest-cov in Python 3.11, runs `manage.py check`, executes tests under the Django development settings with a local SQLite test database, and produces a machine-readable Cobertura `coverage.xml`. A separate Python quality-gate script parses the *current run's* XML and exits with a nonzero status if actual measured line coverage falls below the documented threshold. The workflow uploads coverage evidence for team review and future presentation. This catches reproducible regressions before code is merged, rather than relying solely on local test results.

The repository contains duplicate root and nested application trees. CI intentionally runs from the **repository root** (`manage.py`) to avoid mixing the two. Environment variables select development settings and an in-memory mail backend, so CI is not designed to send external emails or use patient data. Workflow-level `contents: read` limits GitHub token permissions.

### Files owned by Pako

| Path from repository root | Purpose |
|---|---|
| `.github/workflows/pako-quality-gate.yml` | Additive workflow (does not overwrite other members' workflow) |
| `scripts/pako_quality_gate.py` | Parse/validate coverage and optional same-commit mutation evidence; nonzero exit on failure |
| `tests_pako/test_quality_gate.py` | Five isolated tests for the gate logic itself, not patient/application tests |
| `docs/pako/quality_gate_policy.json` | Single visible versioned location for thresholds and enforcement status |
| `docs/pako/WEEK_12_CICD_Quality_Gate.md` | This explanation and integration checklist |

### Threshold decision (provisional until the group approves)

- **Line coverage: proposed minimum 50%.** This is the current **active** threshold in the supplied policy; it is deliberately provisional because current baseline is unmeasured. It may fail with the existing small test suite. Record actual baseline and group agreement before presenting the threshold as a final decision. The score is computed from `coverage.xml` (Cobertura `line-rate`). Branch coverage is collected/reported but is **not currently a separate enforced gate**.
- **Mutation score: proposed minimum 60%.** The quality-gate script supports enforcement, but `enforce_mutation` is intentionally **false** until Maano supplies a repeatable v2 mutation run and same-commit evidence. Therefore the supplied workflow **does not yet satisfy the brief's final mutation gate**. It must not be described as complete.
- Why gates matter: tests running successfully is not sufficient if new changes silently remove assertions or skip critical branches. Coverage catches unexercised source, while mutation measures whether tests distinguish changed behaviour. Neither alone proves correctness; meaningful oracle/assertion review is essential.

### Final mutation integration (must be implemented before Week 12)

1. Maano selects and documents a **bounded real application mutation scope**, tool/version (e.g. mutmut), and reproducible command that runs the *final hybrid* tests. Keep the same scope and mutation policy as v1.
2. Add a workflow step that actually runs mutation testing on the checked-out `GITHUB_SHA` during every push/pull request. Do **not** consume committed or manually edited historical scores.
3. After successful mutation run, create a JSON file from the tool's actual result, containing `score` (percentage 0..100), `commit_sha`, `tool`, and `created_at_utc`. Verify the exporter calculates the score using the stated killed/survived denominator and excludes equivalent mutants only under an explicit consistent policy.
4. Set `"enforce_mutation": true` in `docs/pako/quality_gate_policy.json`, and add the fresh report path to the gate call: `python scripts/pako_quality_gate.py --mutation-json <fresh.json> --commit-sha "$GITHUB_SHA"`. The gate rejects absent or commit-mismatched evidence.
5. Coordinate with Miguel so the CI invocation discovers **unit, integration and BDD/acceptance tests**. Current code demonstrates Pytest discovery but **full BDD automation is not yet verified**. If an acceptance runner needs a separate command, add it explicitly.
6. Record the final agreed thresholds, tool version, full CI URL, successful run SHA, and one deliberately failed gate with a short screenshot/explanation.

### Local verification commands

```bash
# Run from repository root; never from nested hospital-management-system/
python -m pip install -r requirements.txt
python -m pip install 'pytest>=8,<10' 'pytest-django>=4.8,<5' 'pytest-cov>=5,<8'
export DJANGO_ENV=dev DJANGO_SETTINGS_MODULE=hms_project.settings.dev
python manage.py check
python -m unittest discover -s tests_pako -p 'test_*.py' -v
python -m pytest -q --cov=patient --cov=appointment --cov-branch \
  --cov-report=term-missing --cov-report=xml:coverage.xml
python scripts/pako_quality_gate.py --policy docs/pako/quality_gate_policy.json \
  --coverage-xml coverage.xml
```

Windows PowerShell environment configuration:

```powershell
$env:DJANGO_ENV='dev'
$env:DJANGO_SETTINGS_MODULE='hms_project.settings.dev'
$env:SECRET_KEY='local-test-only-secret'
```

### Evidence to paste into the final report (leave unfilled until measured)

| Item | Real result to collect |
|---|---|
| Git commit and run date | `[COMMIT_SHA / DATE]` |
| CI build URL / screenshot | `[URL]` |
| Python, pytest-cov, pytest-django, mutmut versions | `[ACTUAL VERSIONS]` |
| Test totals by level | `[UNIT / INTEGRATION / BDD]` |
| Statement / branch coverage | `[LINE % / BRANCH %]` |
| AI-only mutation v1 and hybrid v2 | `[V1 % / V2 %]` |
| Approved gate thresholds | `[LINE % / MUTATION % / AGREED BY]` |
| Passing and deliberately blocked run | `[PASS URL] / [FAIL URL]` |

### Limitation and integrity statement

The self-tests provided for `pako_quality_gate.py` are genuinely executable and independently verified in the authoring environment. This does **not** verify the full Django suite, GitHub-hosted workflow, or any mutation score. The policy is version-controlled so that later changes to the thresholds are reviewable, and missing mutation evidence is fatal **once enforcement is switched on**. A threshold is never proof of safety; the final report must also discuss incorrect oracle design, equivalence mutants and any excluded tests.
