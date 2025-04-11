import git
import os
from datasets import load_dataset, load_from_disk

def clone_base_commit(repo_name : str, base_commit : str, cloned_path : str):
    repo_link = f"https://github.com/{repo_name}.git"
    if not os.path.exists(cloned_path):
        repo = git.Repo.clone_from(repo_link, cloned_path)
    else:
        repo = git.Repo(cloned_path)
    repo.git.checkout(base_commit)
    return repo

# Load SWE-bench Lite. The dataset is split into 3 tests:
# 1. Dev split: Used during development
# 2. Test split: Reserved for evaluation
# Each row is represented as a dictionary
print("Loading SWE-bench Lite dataset from the web...")
swe_lite = load_dataset("princeton-nlp/SWE-bench_Lite")
print(f"Dataset splits: {swe_lite.keys()}")
dev_split = swe_lite['dev']
test_split = swe_lite['test']

print()
print()

# Print first row of dev split
print("Printing first row of dev split...")
first_dev_row = dev_split[0]
for key, value in first_dev_row.items():
    print(f"-----{key}:-----")
    print(f"\t{value}\n\n")

print()
print()

# Let's clone the first dev repo
print("Cloning first row of dev split...")
sqlfluff = clone_base_commit(first_dev_row["repo"], first_dev_row["base_commit"], "./sqlfluff/")


print()
print()

# Let's check the contents of a repo from the test split with a specific id
matplotlib_id = "matplotlib__matplotlib-18869"
print(f"Checking contents of '{matplotlib_id}'...")
matplotlib_row = next((row for row in test_split if row["instance_id"] == matplotlib_id), None)
for key, value in matplotlib_row.items():
    print(f"-----{key}:-----")
    print(f"\t{value}\n\n")

print()
print()

# Save and load to disk
print("Saving SWE-bench Lite dataset to disk...")
swe_lite.save_to_disk("swe_lite_local")
print("Loading SWE-bench Lite dataset from disk...")
loaded = load_from_disk("swe_lite_local")