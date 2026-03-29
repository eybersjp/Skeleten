import argparse
import sys
import os
from pathlib import Path

# Inject local module dir so imports resolve when called via root orchestrator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skeleten_marrow import run_marrow_probe
from skeleten_graft import GraftEngine
from skeleten_forge import MncForge

class SkeletenSync:
    def __init__(self, src_dir, legacy_path=None, output_dir="./dist"):
        self.src_path = Path(src_dir)
        self.legacy_path = legacy_path
        self.output_dir = output_dir
        self.all_bones = []

    def run(self):
        print("="*80 + "\nSKELETEN // ARCHITECTURAL_RECONSTRUCTION\n" + "-"*80)
        files = [f for f in self.src_path.rglob('*') if f.is_file() and f.suffix in ['.py', '.ts', '.js']]
        for f in files:
            bones = run_marrow_probe(f)
            for b in bones:
                b["id"] = str(f.relative_to(self.src_path))
                self.all_bones.append(b)
        if self.legacy_path:
            self.all_bones = GraftEngine(self.legacy_path).reconcile(self.all_bones)
        MncForge(self.output_dir).forge(self.src_path.name.upper(), self.all_bones, str(self.src_path.absolute()))
        print("="*80)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--src", required=True)
    p.add_argument("--legacy", default=None)
    p.add_argument("--out", default="./dist")
    args = p.parse_args()
    SkeletenSync(args.src, args.legacy, args.out).run()