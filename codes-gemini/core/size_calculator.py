import os
from pathlib import Path


def calculate_directory_size(dir_path: Path) -> int:
    """
    Calcula a soma do tamanho de todos os arquivos dentro do diretório em bytes.
    
    100% Leitura: utiliza os.scandir sem seguir symlinks para evitar ciclos.
    Falhas de permissão ou arquivos travados por outros processos são ignorados 
    de forma transparente sem interromper a soma.
    """
    total_bytes = 0
    stack = [str(dir_path)]

    while stack:
        current_dir = stack.pop()
        try:
            with os.scandir(current_dir) as entries:
                for entry in entries:
                    try:
                        # follow_symlinks=False evita loops em Junctions NTFS e links simbólicos
                        if entry.is_file(follow_symlinks=False):
                            total_bytes += entry.stat(follow_symlinks=False).st_size
                        elif entry.is_dir(follow_symlinks=False):
                            stack.append(entry.path)
                    except (PermissionError, FileNotFoundError, OSError):
                        # Arquivo bloqueado, permissão negada ou caminho longo quebrado: continua
                        continue
        except (PermissionError, FileNotFoundError, OSError):
            # Diretório pai inacessível
            continue

    return total_bytes

