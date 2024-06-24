import os
import sys

def update_version_file(version):
    version_file = os.path.join('hubitat_lock_manager', 'version.py')
    with open(version_file, 'w') as f:
        f.write(f"__version__ = '{version}'\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: update_version.py <version>")
        sys.exit(1)
    version = sys.argv[1]
    update_version_file(version)
