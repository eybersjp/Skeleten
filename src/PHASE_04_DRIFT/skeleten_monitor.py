import os
import stat
from pathlib import Path

# ================================================================================
# SKELETEN // DRIFT_SENTRY // v1.0
# ================================================================================

HOOK_SCRIPT = """#!/usr/bin/env bash
# SKELETEN DRIFT SENTRY PRE-COMMIT HOOK
echo "[*] SKELETEN: Executing Drift Check..."
python run.py --drift-check
if [ $? -ne 0 ]; then
    echo "[!] SKELETEN: Drift detected. Commit aborted."
    exit 1
fi
echo "[+] SKELETEN: Drift check passed."
exit 0
"""

def install_hook():
    print("="*80 + "\nSKELETEN // DRIFT_SENTRY_INSTALL\n" + "-"*80)
    git_dir = Path(".git")
    if not git_dir.exists():
        print("[!] .git directory not found. Initialize git first to use pre-commit blocks.")
        return False
        
    hook_dir = git_dir / "hooks"
    hook_dir.mkdir(exist_ok=True)
    
    pre_commit_path = hook_dir / "pre-commit"
    with open(pre_commit_path, "w") as f:
        f.write(HOOK_SCRIPT)
    
    # Ensure it's executable
    st = os.stat(pre_commit_path)
    os.chmod(pre_commit_path, st.st_mode | stat.S_IEXEC)
    
    print("[+] Pre-commit hook 'Drift Sentry' installed successfully.")
    print("="*80)
    return True

if __name__ == "__main__":
    install_hook()