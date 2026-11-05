# garbage_identification.py
import os

def identify_garbage(path):
    garbage_patterns = ['node_modules', 'target', 'build', '.venv', '__pycache__']
    for pattern in garbage_patterns:
        if pattern in path:
            return 'Lixo Seguro'
    return None
