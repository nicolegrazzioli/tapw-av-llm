# report.py
import os

def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  # Convert to MB

def generate_report(garbage_list):
    for entry in garbage_list:
        print(f"Caminho da Pasta: {entry['path']}")
        print(f"Tamanho: {entry['size']} MB")
        print(f"Tipo de Lixo: {entry['garbage_type']}")
        print(f"URL do GitHub: {entry['backup_url']}")
        print("-" * 40)
