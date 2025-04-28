import os
import shutil
import sys

def copy(src, dst):
    for root, _, files in os.walk(src):
        for f in files:
            try:
                shutil.copy2(
                    os.path.join(root, f),
                    os.path.join(dst, f)
                )
            except Exception:
                continue

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
        
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    copy(src, dst)