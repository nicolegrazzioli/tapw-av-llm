# directory_traversal.py
import os
import errno

def traverse_directory(path):
    for root, dirs, files in os.walk(path, onerror=lambda e: handle_error(e)):
        yield root, dirs, files

def handle_error(e):
    if e.errno == errno.EACCES or e.errno == errno.ENOENT:
        pass
    else:
        raise e
