import os
import pandas as pd
from git import Repo

# Initialize the repository from the current directory
repo = Repo(".")
commits = list(repo.iter_commits())

data = []
for commit in commits:
    for file, stats in commit.stats.files.items():
        data.append({
            "commit_hash": commit.hexsha,
            "author": commit.author.name,
            "file": file,
            "insertions": stats["insertions"],
            "deletions": stats["deletions"],
            "lines_changed": stats["lines"],
        })

df = pd.DataFrame(data)
df.to_csv("git_churn_metrics.csv", index=False)
print(f"Extracted {len(df)} file-change records successfully into git_churn_metrics.csv!")