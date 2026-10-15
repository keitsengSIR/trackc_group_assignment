import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# 1. Load the extracted git churn metrics
df = pd.read_csv("git_churn_metrics.csv")

# 2. Aggregate metrics by file (Total Insertions, Total Deletions, Total Lines Changed, Commit Count)
file_agg = df.groupby("file").agg(
    commit_count=("commit_hash", "count"),
    total_insertions=("insertions", "sum"),
    total_deletions=("deletions", "sum"),
    total_lines_changed=("lines_changed", "sum")
).reset_index()

# 3. Create a heuristic target label for defects (e.g., files modified across multiple commits or with high churn are higher risk)
# Here we label files with above-median churn/commits as defect-prone (1) vs low-risk (0)
median_churn = file_agg["total_lines_changed"].median()
file_agg["is_defective"] = (file_agg["total_lines_changed"] > median_churn).astype(int)

# 4. Prepare features (X) and target (y)
X = file_agg[["commit_count", "total_insertions", "total_deletions", "total_lines_changed"]]
y = file_agg["is_defective"]

# Handle edge cases if dataset is small
if len(file_agg) > 5:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 5. Train the Scikit-Learn Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 6. Evaluate the model
    y_pred = model.predict(X_test)
    print("--- Defect Prediction Model Evaluation ---")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    # Feature importances
    importances = model.feature_importances_
    for feature, imp in zip(X.columns, importances):
        print(f"Feature Importance [{feature}]: {imp:.4f}")
else:
    print("Aggregated files data is too small for train_test_split. Review aggregated file count.")