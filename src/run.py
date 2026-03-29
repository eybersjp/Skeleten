import sys
import os
import argparse
import subprocess
from pathlib import Path

# Auto-relaunch inside isolated SKELETEN venv if available
venv_win = os.path.abspath(os.path.join(".skeleten", "venv", "Scripts", "python.exe"))
venv_unix = os.path.abspath(os.path.join(".skeleten", "venv", "bin", "python"))
exec_path = os.path.abspath(sys.executable)
if exec_path != venv_win and exec_path != venv_unix:
    if os.path.exists(venv_win):
        sys.exit(subprocess.call([venv_win] + sys.argv))
    elif os.path.exists(venv_unix):
        sys.exit(subprocess.call([venv_unix] + sys.argv))

# Add root dir to ensure cross-phase module resolution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def execute_phase(name, func, *args):
    print(f"\n[{name}] {'='*60}")
    try:
        func(*args)
        print(f"[{name}] SUCCESS")
    except Exception as e:
        print(f"[{name}] FAILED (Module Compatibility Error): {e}")

def phase_00():
    from PHASE_00_INTENT.skeleten_wizard import run_wizard
    run_wizard()

def phase_01():
    from PHASE_01_CORE.skeleten_sync import SkeletenSync
    sync = SkeletenSync(src_dir=".", output_dir="./PHASE_01_CORE/dist")
    sync.run()

def phase_02():
    from PHASE_02_VECTOR.skeleten_vector_graft import VectorGraft
    import numpy as np
    vg = VectorGraft()
    print("VectorGraft Engine ready embeddings module: ", vg.model)

def phase_03():
    from PHASE_03_GEN.skeleten_autodoc import AutoDoc
    doc = AutoDoc("./PHASE_01_CORE/dist/skeleten_mnc.json")
    md = doc.to_markdown()
    with open("SKELETEN_API_REFERENCE.md", "w", encoding='utf-8') as f:
        f.write(md)
    print("Generated SKELETEN_API_REFERENCE.md via Generator Phase.")

def phase_04():
    from PHASE_04_DRIFT.skeleten_monitor import install_hook
    install_hook()

def drift_check():
    print("Running SKELETEN DRIFT CHECK...")
    mnc_path = "./PHASE_01_CORE/dist/skeleten_mnc.json"
    if not os.path.exists(mnc_path):
        print("FAIL: MNC JSON missing.")
        sys.exit(1)
        
    import json
    with open(mnc_path, 'r') as f:
        data = json.load(f)
        
    pts = data.get("pts", [])
    if not pts and "about" in data:
        pts = data["about"]
        
    stale_count = sum(1 for p in pts if p.get("stl", False) or p.get("identifier") == "STALE")
    stale_ratio = stale_count / max(len(pts), 1)
    
    STATIC_STALE_TOLERANCE = 0.15
    
    if stale_ratio > STATIC_STALE_TOLERANCE:
        print(f"[!] SKELETEN: Severe intent drift detected. {stale_ratio*100:.1f}% of codebase lacks updated rationales.")
        print(f"    THRESHOLD: {STATIC_STALE_TOLERANCE*100}%  |  CURRENT: {stale_ratio*100:.1f}%")
        print("    STATUS: COMMIT ABORTED. Please update documentation.")
        sys.exit(1)
        
    print(f"[+] SKELETEN: Intent Drift within acceptable bounds ({stale_ratio*100:.1f}%).")
    print("    STATUS: COMMIT ALLOWED.")
    sys.exit(0)

def health_check():
    import SKELETEN_HEALTH_CHECK
    hc = SKELETEN_HEALTH_CHECK.HealthCheck()
    hc.run()
    if hc.errors > 0:
        print("Health Check Failed!")
        sys.exit(1)

def display_logo():
    ORANGE = '\033[38;5;208m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    
    logo = f"""
{ORANGE}      _________________
     /                /
    /      __________/
   /      /
  /      /____________      _  _________  _      _________  _________  _      _
 /                  /     | |/ /|  ____|| |    |  ____||__   __||  ____|| \\    | |
/___________      _/      | ' / | |__   | |    | |__      | |   | |__   |  \\   | |
           /     /        |  <  |  __|  | |    |  __|     | |   |  __|  | |\\ \\  | |
 _________/     /         | . \\ | |____ | |____| |____    | |   | |____ | | \\ \\ | |
/______________/          |_|\\_\\|______||______||______|   |_|   |______||_|  \\___|

  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _   [✓]
{RESET}"""
    print(logo)

if __name__ == "__main__":
    display_logo()
    
    p = argparse.ArgumentParser()
    p.add_argument("--drift-check", action="store_true")
    p.add_argument("--health-check", action="store_true")
    p.add_argument("--wizard", action="store_true")
    args = p.parse_args()

    if args.drift_check:
        drift_check()
    elif args.health_check:
        health_check()
    elif args.wizard:
        from PHASE_00_INTENT.skeleten_wizard import run_wizard
        run_wizard()
    else:
        print("\n" + "="*80)
        print("SKELETEN // MASTER_SEQUENCER // v4.0")
        print("="*80)
        
        execute_phase("PHASE_01_CORE", phase_01)
        execute_phase("PHASE_02_VECTOR", phase_02)
        execute_phase("PHASE_03_GEN", phase_03)
        execute_phase("PHASE_04_DRIFT", phase_04)
        
        print("\n[VALIDATION] Running Health Check...")
        health_check()
        
        print("\n" + "="*80)
        print("SKELETEN: SYSTEM SECURED AND PRODUCTION READY")
        print("="*80)
