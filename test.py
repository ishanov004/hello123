import os
import subprocess
from dotenv import load_dotenv

# === Load .env file ===
load_dotenv()

# === CONFIGURATION ===
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME = os.getenv("REPO_NAME")
TOKEN = os.getenv("GITHUB_TOKEN")
EMAIL = os.getenv("GIT_EMAIL")
NAME = os.getenv("GIT_NAME")
BRANCH_NAME = "main"

# === Local folder ===
LOCAL_FOLDER = r"C:\Users\misha\OneDrive\Рабочий стол\servers.tm"
os.chdir(LOCAL_FOLDER)

repo_url = f"https://{GITHUB_USERNAME}:{TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

def run_git(cmd):
    try:
        print(f"👉 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error:\n{e.stderr}")

# === Safe Git push ===
run_git(["git", "init"])
run_git(["git", "remote", "remove", "origin"])
run_git(["git", "remote", "add", "origin", repo_url])
run_git(["git", "config", "user.email", EMAIL])
run_git(["git", "config", "user.name", NAME])
run_git(["git", "add", "."])
run_git(["git", "commit", "-m", "🔥 Safe push from local project"])
run_git(["git", "branch", "-M", BRANCH_NAME])
run_git(["git", "push", "--force", "-u", "origin", BRANCH_NAME])

print("✅ DONE! Repo is securely pushed.")
