import os
import json
import sys
from pathlib import Path

# ================================================================================
# SKELETEN // SYSTEM_HEALTH_CHECK // v1.0
# ================================================================================

class HealthCheck:
    def __init__(self):
        self.root = Path(".")
        self.phases = ["PHASE_01_CORE", "PHASE_02_VECTOR", "PHASE_03_GEN"]
        self.errors = 0

    def log(self, msg, status="INFO"):
        colors = {"PASS": "\033[92m", "FAIL": "\033[91m", "INFO": "\033[94m"}
        reset = "\033[0m"
        print(f"{colors.get(status, '')}[{status}] {msg}{reset}")

    def check_structure(self):
        """Verify all phase directories exist."""
        for phase in self.phases:
            if (self.root / phase).exists():
                self.log(f"Directory found: {phase}", "PASS")
            else:
                self.log(f"Missing directory: {phase}", "FAIL")
                self.errors += 1

    def verify_mnc_schema(self, mnc_path):
        """Validate MNC v1.9 JSON-LD structure."""
        try:
            with open(mnc_path, 'r') as f:
                data = json.load(f)
            required = ["@context", "nm", "pts"]
            if all(k in data for k in required):
                self.log("MNC Schema v1.9 validation: SUCCESS", "PASS")
            else:
                self.log("MNC Schema mismatch: MISSING_REQUIRED_KEYS", "FAIL")
                self.errors += 1
        except Exception as e:
            self.log(f"MNC Read Error: {e}", "FAIL")
            self.errors += 1

    def run(self):
        print("="*80 + "\nSKELETEN // SYSTEM_INTEGRITY_CHECK\n" + "-"*80)
        
        self.check_structure()
        
        # Check for Phase 1 Output
        mnc_file = self.root / "PHASE_01_CORE" / "dist" / "skeleten_mnc.json"
        if mnc_file.exists():
            self.verify_mnc_schema(mnc_file)
        else:
            self.log("MNC Output not found. Run Phase 1 first.", "INFO")

        print("-"*80)
        if self.errors == 0:
            self.log("SYSTEM_HEALTH: NOMINAL // READY_FOR_DEPLOYMENT", "PASS")
        else:
            self.log(f"SYSTEM_HEALTH: CRITICAL // {self.errors} ERRORS_FOUND", "FAIL")
        print("="*80)

if __name__ == "__main__":
    HealthCheck().run()