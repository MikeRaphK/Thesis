import requests
import sys

def fetch_repo_files(username : str, repo_name : str, path : str = ""):
    """
    Fetches all files of a public GitHub repo at a given path.  
    Also fetches files found in folders and subfolders.  
    Returns a list of files in JSON format if response was successful, None otherwise.
    """
    
    # Build GitHub’s REST API url
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}"

    # Get a response
    response = requests.get(url)

    # If the request fails, print error and return None
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        return None

    repo_files = []
    repo_contents = response.json()
    
    # Add files to list. Recursively call the function to find files in directories
    for item in repo_contents:
        if item["type"] == "file":
            repo_files.append(item)
        else:
            dir_files = fetch_repo_files(username, repo_name, item["path"])
            # Check if request failed
            if dir_files == None:
                return None
            repo_files += dir_files

    return repo_files

def print_file(file : dict) -> None:
    """
    Prints all pairs of keys and values of given file
    """
    for key in file:
        print(f"{key} = {file[key]}")

if __name__ == "__main__":
    # Read arguments
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <owner username> <repo name>")
        exit()
    username = sys.argv[1]
    repo_name = sys.argv[2]

    # Get files of repo
    repo_files = fetch_repo_files(username, repo_name)
    if repo_files == None:
        exit()
    
    # Print contents
    for file in repo_files:
        print_file(file)
        print('-------------------------------------')
    