import os
import subprocess

def get_latest_tag():
    try:
        return subprocess.check_output(['git', 'describe', '--tags']).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        return None

def update_version_file(version):
    version_file = os.path.join('hubitat_lock_manager', 'version.py')
    with open(version_file, 'w') as f:
        f.write(f"__version__ = '{version}'\n")

if __name__ == "__main__":
    tag = get_latest_tag()
    if tag:
        update_version_file(tag)
