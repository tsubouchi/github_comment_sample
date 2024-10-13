import os
from github import Github
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
if not token:
    print("GITHUB_TOKEN is not set")
    exit(1)
g = Github(token)
user = g.get_user()
print(f"Logged in as: {user.login}")
repo_name = input("Enter repository name (e.g., username/repo): ")
try:
    repo = g.get_repo(repo_name)
except Exception as e:
    print(f"Error accessing repository: {e}")
    exit(1)
print(f"Accessing repository: {repo.full_name}")
branches = repo.get_branches()
print("Branches:")
for branch in branches:
    print(f"- {branch.name}")
file_path = input("Enter the path of the file to update (e.g., README.md): ")
try:
    contents = repo.get_contents(file_path, ref="main")
    file_content = contents.decoded_content.decode()
    new_content = file_content + "\n\nThis is a test update."
    repo.update_file(contents.path, "Update file via script", new_content, contents.sha, branch="main")
    print(f"Updated file {file_path}")
except Exception as e:
    print(f"Error updating file: {e}")
    exit(1)
print("Creating a pull request...")
pr = repo.create_pull(title="Test PR", body="This is a test pull request.", head="main", base="main")
print(f"Pull request created: #{pr.number} {pr.title}")
issues = repo.get_issues(state='open')
print("Open issues:")
for issue in issues:
    print(f"- #{issue.number} {issue.title}")
print("Creating a new issue...")
issue_title = "Demo Issue"
issue_body = "This is a demo issue created by the script."
issue = repo.create_issue(title=issue_title, body=issue_body)
print(f"Issue created: #{issue.number} {issue.title}")
