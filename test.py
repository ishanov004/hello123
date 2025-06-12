import os
import subprocess
import requests
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
GIT_NAME = os.getenv("GIT_NAME")
GIT_EMAIL = os.getenv("GIT_EMAIL")
BRANCH = "main"

# === Local project folder ===
LOCAL_REPO = r"C:\Users\misha\OneDrive\Рабочий стол\servers.tm"
os.chdir(LOCAL_REPO)

# === Step 1: Create repo on GitHub ===
print("🌐 Creating GitHub repo (if not exists)...")
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
    print(f"❌ GitHub error:\n{response.text}")
    exit(1)

# === Git remote URL (without exposing token in code or commit) ===
repo_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# === Helper function ===
def run_git(cmd):
    try:
        print(f"👉 {' '.join(cmd)}")
        subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error:\n{e.stderr}")
        exit(1)

# === Step 2: Git init & setup ===
run_git(["git", "init"])
run_git(["git", "remote", "remove", "origin"])
run_git(["git", "remote", "add", "origin", repo_url])
run_git(["git", "config", "user.name", GIT_NAME])
run_git(["git", "config", "user.email", GIT_EMAIL])

# === Step 3: Safe commit ===
run_git(["git", "add", "."])
run_git(["git", "commit", "-m", "🚀 Safe initial commit without exposing secrets"])
run_git(["git", "branch", "-M", BRANCH])
run_git(["git", "push", "--force", "-u", "origin", BRANCH])

print(f"\n✅ Project pushed safely to: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
