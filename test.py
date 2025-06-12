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

# === Path to your local project ===
LOCAL_REPO = r"C:\Users\misha\OneDrive\Рабочий стол\servers.tm"
os.chdir(LOCAL_REPO)

# === GitHub Repo URL with authentication ===
repo_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# === GitHub API: Create repo ===
print("🌐 Checking GitHub repo...")
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
    print(f"❌ GitHub API error:\n{response.status_code} - {response.text}")
    exit(1)

# === Git runner with output ===
def run_git(cmd):
    try:
        print(f"👉 {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        if result.stdout.strip():
            print("🟢 STDOUT:\n", result.stdout)
        if result.stderr.strip():
            print("🟡 STDERR:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git failed:\n{e.stderr}")
        exit(1)

# === Step-by-step Git actions ===
run_git(["git", "init"])
run_git(["git", "remote", "remove", "origin"])
run_git(["git", "remote", "add", "origin", repo_url])
run_git(["git", "config", "user.name", GIT_NAME])
run_git(["git", "config", "user.email", GIT_EMAIL])
run_git(["git", "add", "."])

# Try to commit
print("📝 Trying to commit...")
commit_result = subprocess.run(
    ["git", "commit", "-m", "🚀 Safe initial commit"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding='utf-8'
)

if "nothing to commit" in commit_result.stderr.lower():
    print("⚠️ Nothing to commit! Maybe already committed. Skipping...")
else:
    print("✅ Commit successful.")
    print(commit_result.stdout)
    print(commit_result.stderr)

# Rename and push
run_git(["git", "branch", "-M", BRANCH])
run_git(["git", "push", "--force", "-u", "origin", BRANCH])

print(f"\n✅ DONE! Project pushed to: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
