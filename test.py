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

# === Local repo folder ===
LOCAL_REPO_PATH = r"C:\Users\misha\OneDrive\Рабочий стол\servers.tm"
os.chdir(LOCAL_REPO_PATH)

# === GitHub repo API URL ===
REPO_API_URL = "https://api.github.com/user/repos"

# === Create GitHub repo if it doesn't exist ===
print("📡 Creating repository on GitHub...")
response = requests.post(
    REPO_API_URL,
    headers={"Authorization": f"token {GITHUB_TOKEN}"},
    json={"name": REPO_NAME, "private": False}
)

if response.status_code == 201:
    print(f"✅ Repository '{REPO_NAME}' created successfully!")
elif response.status_code == 422:
    print(f"ℹ️ Repo already exists. Continuing...")
else:
    print(f"❌ Failed to create repo: {response.text}")
    exit(1)

# === Prepare repo URL ===
repo_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# === Git commands ===
def run(cmd):
    try:
        print(f"👉 Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        print(f"❌ {e.stderr}")

# === Git setup ===
run(["git", "init"])
run(["git", "remote", "remove", "origin"])
run(["git", "remote", "add", "origin", repo_url])
run(["git", "config", "user.email", GIT_EMAIL])
run(["git", "config", "user.name", GIT_NAME])
run(["git", "add", "."])
run(["git", "commit", "-m", "🚀 Initial safe commit"])
run(["git", "branch", "-M", BRANCH])

# === Clean .env and script from history ===
run(["git", "rm", "--cached", ".env", "push_to_github.py"])
run(["git", "commit", "-m", "🚫 Remove secrets"])

run([
    "git", "filter-branch", "--force", "--index-filter",
    "git rm --cached --ignore-unmatch .env push_to_github.py",
    "--prune-empty", "--tag-name-filter", "cat", "--", "--all"
])

# === Final push ===
run(["git", "push", "--force", "-u", "origin", BRANCH])
print("✅ Project safely pushed to GitHub!")

