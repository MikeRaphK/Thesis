import os
import re
import requests
import shutil

from git import Repo
from typing import List, Dict, Tuple


def parse_owner_name_default_branch(repo_url: str, GITHUB_TOKEN: str) -> Tuple[str, str, str]:
    """
    Parse the owner, repository name, and default branch from a GitHub repository URL.

    Args:
        repo_url (str): The GitHub repository URL.

    Returns:
        Tuple[str, str, str]: A tuple containing the repository owner, name, and default branch.
        If the URL is invalid or the repo is not found, returns (None, None, None).
    """
    match = re.match(r'https?://github\.com/([^/]+)/([^/]+)(?:/|$)', repo_url)
    if not match:
        return None, None
    owner, repo =  match.group(1), match.group(2)

    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = { "Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github+json" }
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get default branch. Error: {response.status_code} {response.text}")
    default_branch = response.json().get("default_branch", "main")
    return owner, repo, default_branch


def get_open_issues(owner: str, name: str) -> List[Dict[str, str]]:
    """
    Get open issues from a GitHub repository.

    Args:
        owner (str): The owner of the repository.
        name (str): The name of the repository.

    Returns:
        List[Dict[str, str]]: A list of open issues, each as a dictionary with 'title', 'body' and 'number'.
    """
    issues_url = f"https://api.github.com/repos/{owner}/{name}/issues"
    params = {'state': 'open', 'per_page': 100}
    response = requests.get(issues_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to get issues. Error: {response.status_code} {response.text}")
    
    # Get title, body and number of each issue while ignoring pull requests
    issues = []
    for issue in response.json():
        if 'pull_request' not in issue:
            element = {"title": issue["title"], "body": issue.get("body", ""), "number": issue["number"]}
            issues.append(element)
            
    return issues


def clone_repo(repo_url: str, repo_path: str) -> Repo:
    """Clones a Git repository to a specified local path, removing any existing directory.

    Args:
        repo_url (str): The URL of the Git repository to clone.
        repo_path (str): The local file path where the repository should be cloned.

    Returns:
        Repo: A GitPython Repo object representing the cloned repository.
    """
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    Repo.clone_from(repo_url, repo_path)
    return Repo(repo_path)


def create_pr(repo: Repo, commit_msg:str, owner: str, repo_name: str, GITHUB_TOKEN: str, title: str, body: str, base_branch: str) -> None:
    """Stages all changes, commits them, pushes to the current branch, and creates a pull request on GitHub.

    The function assumes the current branch (i.e., `repo.active_branch.name`) is the source (head) of the pull request.
    It pushes the commit to the remote if needed, and then makes a GitHub API call to open a PR into the specified base branch.

    Args:
        repo (Repo): The GitPython Repo object representing the local repository.
        commit_msg (str): The commit message to use for the staged changes.
        owner (str): The GitHub username or organization that owns the repository.
        repo_name (str): The name of the target GitHub repository.
        GITHUB_TOKEN (str): A GitHub personal access token used for authentication.
        title (str): The title of the pull request.
        body (str): The body/description of the pull request.
        base_branch (str): The name of the branch to merge into (usually 'main' or 'master').
    """
    repo.git.add(".")
    repo.index.commit(commit_msg)
    if repo.active_branch.tracking_branch() is None:
        repo.git.push("--set-upstream", "origin", repo.active_branch.name)
    else:
        repo.git.push()

    pr_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
    data = {
        "title": title,
        "body": body,
        "head": repo.active_branch.name,
        "base": base_branch
    }
    response = requests.post(pr_url, headers=headers, json=data)
    if response.status_code != 201:
        raise Exception(f"Failed to get default branch. Error: {response.status_code} {response.text}")