from langchain_community.tools import ReadFileTool, WriteFileTool, ListDirectoryTool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

import json
import os
import re
import sys
from dotenv import load_dotenv

import github_utils as ghu
from build_graph import build_graph

# Load from .env
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    # Read arguments
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <GitHub URL>")
        sys.exit(1)

    # Get repo URL and check if it is valid
    print("Checking if the GitHub URL is valid...\n")
    repo_url = sys.argv[1]
    owner, repo_name, default_branch = ghu.parse_owner_name_default_branch(repo_url, GITHUB_TOKEN)
    if not owner and not repo_name:
        print(f"Invalid GitHub URL: {repo_url}")
        sys.exit(1)
    
    # Get open issues
    print("Getting open issues...\n")
    open_issues = ghu.get_open_issues(owner, repo_name)
    if not open_issues:
        print(f"No open issues found in {repo_url}. Exiting...")
        sys.exit(1)
    first_issue = open_issues[0]

    # Clone repo
    print("Cloning repo...\n")
    repo_path = "./cloned_repo/"
    repo = ghu.clone_repo(repo_url, repo_path)

    # Create (or checkout) to the new branch
    branch_name = "llm-patcher"
    print(f"Branching to '{branch_name}'...\n")
    if branch_name in [b.name for b in repo.branches]:
        repo.git.checkout(branch_name)
        repo.git.pull()
    else:
        repo.git.checkout("-b", branch_name)

    # Create the graph
    print("Initializing ReAct graph...\n")
    model = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
    tools = [ReadFileTool(verbose=True), WriteFileTool(verbose=True), ListDirectoryTool(verbose=True)]
    APP = build_graph(tools=tools, llm=model)

    # Initialize system message and query
    print("Initializing chat history...\n")
    chat_history = []
    system_message = SystemMessage(content="""
        You are an AI software engineer. Your task is to automatically fix issues in a local GitHub repository located at ./cloned_repo. For each task:
            1. Read and understand the GitHub issue provided to you.
            2. Locate the relevant part(s) of the codebase inside ./cloned_repo that need to be changed.
            3. Modify the code to resolve the issue while maintaining functionality, clarity, and style.
            4. Generate a concise and informative git commit message describing the fix.
            5. Prepare a pull request summary explaining what was fixed, how it was fixed, and any tests added or run.
        Constraints:
            1. Only make changes necessary to fix the issue.
            2. Prefer minimal, safe, and testable changes.
            3. Do not introduce unrelated modifications.
            4. Assume the repository uses standard Git practices.
        Respond with a JSON object containing the following fields:
            - "modified_files": The list of modified files.
            - "commit_msg": The commit message.
            - "pr_title": The pull request title.
            - "pr_body": The pull request body. Make sure to include the issue number in the body.
    """)
    chat_history.append(system_message)
    query = HumanMessage(content=f"""
        Issue Title: {first_issue['title']}
        Issue Body: {first_issue['body']}
        Issue Number: {first_issue['number']}
    """)
    chat_history.append(query)

    # Invoke the LLM
    print("Invoking LLM...\n")
    output_state = APP.invoke({"messages" : chat_history})
    content = output_state["messages"][-1].content
    print(f"\n\nChatGPT response: {content}\n")

    # Create a pull request
    print("Creating pull request...\n")
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)  # Remove opening fence
        content = re.sub(r"\s*```$", "", content)          # Remove closing fence
    content_json = json.loads(content)
    ghu.create_pr(repo, content_json["commit_msg"], owner, repo_name, GITHUB_TOKEN, content_json["pr_title"], content_json["pr_body"], default_branch)
    print("Pull request created successfully!")    