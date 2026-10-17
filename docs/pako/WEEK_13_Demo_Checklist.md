# PAKO | Week 13 (17 Nov 2026) | CI/CD live demonstration checklist

**Status:** Plan only, not evidence of a completed demo.

- [ ] Confirm all test levels have executable CI steps (unit / integration / BDD acceptance).
- [ ] Confirm same-run mutmut score and line coverage gates are both **enforced** (policy: `enforce_mutation=true`).
- [ ] Run and save a passing workflow, URL, commit SHA and linked artifacts.
- [ ] Demonstrate a deliberate failing test or a reversible, isolated threshold change on a demo branch; show the gate prevents passing and explain *why*. Revert before merge.
- [ ] Point out coverage XML, mutation exporter output and exact measured test run.
- [ ] Explain how the run handles synthetic patient data and avoids secrets/real PII.
- [ ] Show where to modify thresholds and where changes must be reviewed.
- [ ] Record final decisions/screenshots and hand them to Thabiso for appendices.

Suggested Pako speaking segment (1–2 minutes): "The pipeline is triggered by pushes and pull requests. It checks the Django application and then executes our hybrid tests. Coverage and mutation scores are evaluated against group-approved thresholds, and a failed gate blocks the build. Here is the successful run, here is a deliberately blocked run, and here are the artifacts tied to the tested commit."

**Do not use that script as a statement of completed work before the workflow and demo actually succeed.**
