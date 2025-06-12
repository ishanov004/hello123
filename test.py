import os
import subprocess

# === CONFIGURATION ===
GITHUB_USERNAME = "ishanov004"  # ✅ Change to your GitHub username
REPO_NAME = "project7"          # ✅ Change to your repo name
TOKEN = "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"  # 🔐 Your GitHub token
BRANCH_NAME = "main"
EMAIL = "m.ishanov004@gmail.com"        # ✅ Set your GitHub email
NAME = "Myrat"                  # ✅ Your GitHub name

# === Local folder to push ===
LOCAL_FOLDER = r"C:\Users\misha\OneDrive\Рабочий стол\servers.tm"
os.chdir(LOCAL_FOLDER)

# === GitHub repo URL with token ===
repo_url = f"https://{GITHUB_USERNAME}:{TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# === Helper to run git commands ===
def run_git(cmd):
    try:
        print(f"👉 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error:\n{e.stderr}")

# === Git steps ===
run_git(["git", "init"])
run_git(["git", "remote", "remove", "origin"])  # In case it exists
run_git(["git", "remote", "add", "origin", repo_url])
run_git(["git", "config", "user.email", EMAIL])
run_git(["git", "config", "user.name", NAME])
run_git(["git", "add", "."])
run_git(["git", "commit", "-m", "🔥 Full overwrite from local project"])
run_git(["git", "branch", "-M", BRANCH_NAME])
run_git(["git", "push", "--force", "-u", "origin", BRANCH_NAME])  # ⚠️ Force push = delete remote changes

print("✅ DONE! Repo is now fully overwritten with your local folder.")
