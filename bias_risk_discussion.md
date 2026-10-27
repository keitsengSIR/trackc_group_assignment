# Bias-Risk Discussion in Defect Prediction (Track C)

When deploying machine learning classifiers to predict defect-prone modules or flag "risky" code contributions in healthcare software repositories, several ethical and operational biases must be considered:

1. **Contributor Bias**: Models trained heavily on commit history and author activity metrics can unfairly penalize junior developers, part-time contributors, or developers working on complex legacy modules, misinterpreting frequency of edits as poor code quality.
2. **Historical Data Bias**: If past bug reports under-reported defects in certain experimental modules (e.g., UI intake forms) while over-reporting backend database bugs, the classifier will learn skewed risk weights.
3. **Over-Reliance on Complexity Metrics**: High lines of code (LOC) or cyclomatic complexity do not always equate to buggy code. Flagging modules automatically without human code review can create toxic developer friction and false positives.
**Mitigation**: Defect predictors in our pipeline are used strictly as a **prioritization heuristic** to guide human testers toward high-risk areas, never as an automated penalty tool against contributors.