import os
import subprocess
import requests
from dotenv import load_dotenv

# === Load secrets from .env ===
load_dotenv()
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
GIT_NAME = os.getenv("GIT_NAME")
GIT_EMAIL = os.getenv("GIT_EMAIL")
BRANCH = "main"

# === Local folder ===
LOCAL_REPO = r"C:\Users\misha\OneDrive\Рабочий стол\servers.tm"
os.chdir(LOCAL_REPO)

# === Step 1: Create GitHub repo ===
print("🌐 Creating GitHub repo...")
response = requests.post(
    "https://api.github.com/user/repos",
    headers={"Authorization": f"token {GITHUB_TOKEN}"},
    json={"name": REPO_NAME, "private": False}
)

if response.status_code == 201:
    print(f"✅ Repo '{REPO_NAME}' created.")
elif response.status_code == 422:
    print(f"ℹ️ Repo '{REPO_NAME}' already exists.")
else:
    print(f"❌ Failed to create repo:\n{response.text}")
    exit(1)

# === Repo URL for push ===
repo_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# === Git helper ===
def run_git(cmd):
    try:
        print(f"👉 {' '.join(cmd)}")
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error:\n{e.stderr}")
        exit(1)

# === Step 2: Git initialization & setup ===
run_git(["git", "init"])
run_git(["git", "remote", "remove", "origin"])
run_git(["git", "remote", "add", "origin", repo_url])
run_git(["git", "config", "user.name", GIT_NAME])
run_git(["git", "config", "user.email", GIT_EMAIL])

# === Step 3: Add and commit all files ===
run_git(["git", "add", "."])
run_git(["git", "commit", "-m", "🚀 Initial safe commit"])

# === Step 4: Remove sensitive files from index ===
run_git(["git", "rm", "--cached", ".env", "push_to_github.py"])
run_git(["git", "commit", "-m", "🚫 Remove sensitive files"])

# === Step 5: Clean up history ===
run_git([
    "git", "filter-branch", "--force", "--index-filter",
    "git rm --cached --ignore-unmatch .env push_to_github.py",
    "--prune-empty", "--tag-name-filter", "cat", "--", "--all"
])

# === Step 6: Push to GitHub ===
run_git(["git", "branch", "-M", BRANCH])
run_git(["git", "push", "--force", "-u", "origin", "BRANCH"])

print(f"\n✅ DONE! Project pushed to: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
