# main.py
import os
from directory_traversal import traverse_directory
from garbage_identification import identify_garbage
from backup_check import check_backup
from report import generate_report

def get_input_path():
    path = input("Digite o caminho inicial (Enter para usar 'C:\\Users\\nicol\\nicolegrazzioli\\tapw-av-llm'): ")
    if not path:
        path = 'C:\\Users\\nicol\\nicolegrazzioli\\tapw-av-llm'
    return path

def main():
    path = get_input_path()
    garbage_list = []
    for root, dirs, files in traverse_directory(path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            garbage_type = identify_garbage(dir_path)
            if garbage_type:
                backup_url = check_backup(dir_path)
                garbage_list.append({
                    'path': dir_path,
                    'size': get_directory_size(dir_path),
                    'garbage_type': garbage_type,
                    'backup_url': backup_url
                })

    generate_report(garbage_list)

if __name__ == "__main__":
    main()