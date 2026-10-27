"""
Track C: Defect-Prediction Classifier using scikit-learn
Analyzes code metrics (churn, cyclomatic complexity, lines of code) 
to predict bug-prone modules in the healthcare repository.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def generate_mock_repo_metrics(n_samples=500):
    """Generates synthetic commit/churn and complexity metrics for repository files."""
    np.random.seed(42)
    # Features: [Lines of Code (LOC), Cyclomatic Complexity, Commit Count, Code Churn Rate]
    X = np.random.rand(n_samples, 4)
    X[:, 0] = X[:, 0] * 500 + 20   # LOC between 20 and 520
    X[:, 1] = X[:, 1] * 15 + 1     # Complexity between 1 and 16
    X[:, 2] = X[:, 2] * 40 + 2     # Commits between 2 and 42
    X[:, 3] = X[:, 3] * 100        # Churn rate
    
    # Target: Defect prone (1) or Clean (0) based on high complexity and churn
    y = ((X[:, 1] > 10) & (X[:, 3] > 60) | (X[:, 0] > 400)).astype(int)
    return X, y

def train_defect_predictor():
    print("[*] Loading repository metrics for defect prediction...")
    X, y = generate_mock_repo_metrics()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print("\n--- Defect Predictor Evaluation Report ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(classification_report(y_test, y_pred))
    
    return model

if __name__ == "__main__":
    train_defect_predictor()