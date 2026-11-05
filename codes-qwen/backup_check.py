# backup_check.py
import os

def check_backup(path):
    git_path = os.path.join(path, '.git')
    if os.path.exists(git_path):
        with open(os.path.join(git_path, 'config'), 'r') as f:
            for line in f:
                if 'url' in line:
                    return line.split('=')[1].strip().strip('"')
    return None
