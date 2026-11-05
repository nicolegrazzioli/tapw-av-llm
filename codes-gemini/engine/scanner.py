import os
from pathlib import Path
from typing import Dict, Generator, Set

from core.models import WasteReportItem, WasteSignature
from core.size_calculator import calculate_directory_size
from git.inspector import GitInspector


class WasteScanner:
    """
    Motor de varredura recursiva de diretórios com poda de árvore (pruning).
    Garante que diretórios identificados como lixo não sejam escaneados internamente.
    """

    def __init__(self, signatures: Dict[str, WasteSignature]):
        self.signatures = signatures
        self.git_inspector = GitInspector()

    def scan(self, target_root: Path) -> Generator[WasteReportItem, None, None]:
        """
        Varre o target_root emitindo diagnósticos sob demanda (streaming via generator).
        Não interrompe execução por PermissionError ou arquivos inacessíveis.
        """
        stack = [target_root]
        visited_dirs: Set[str] = set()

        while stack:
            current_path = stack.pop()
            current_str = str(current_path)

            if current_str in visited_dirs:
                continue
            visited_dirs.add(current_str)

            try:
                with os.scandir(current_path) as entries:
                    for entry in entries:
                        try:
                            # Ignora links simbólicos para evitar loops ou travessias fora do alvo
                            if not entry.is_dir(follow_symlinks=False):
                                continue

                            folder_name = entry.name
                            folder_path = Path(entry.path)

                            # Evita inspecionar o interior da própria pasta .git
                            if folder_name == ".git":
                                continue

                            # Caso 1: A pasta corresponde a uma assinatura de lixo conhecida
                            if folder_name in self.signatures:
                                signature = self.signatures[folder_name]
                                
                                # Calcula tamanho da pasta de lixo
                                size_bytes = calculate_directory_size(folder_path)
                                
                                # Descobre se o projeto tem Git e remote URL
                                git_root, remote_url = self.git_inspector.inspect_path(folder_path)

                                yield WasteReportItem(
                                    folder_path=folder_path,
                                    size_bytes=size_bytes,
                                    signature=signature,
                                    git_remote_url=remote_url,
                                    git_project_root=git_root,
                                )

                                # PODA: Não adiciona `folder_path` à stack.
                                # Evita varrer subpastas de um node_modules ou build.
                                continue

                            # Caso 2: Diretório de código normal -> agenda para descida recursiva
                            stack.append(folder_path)

                        except (PermissionError, FileNotFoundError, OSError):
                            # Pasta sem permissão de leitura ou caminho inacessível no Windows
                            continue

            except (PermissionError, FileNotFoundError, OSError):
                # O próprio `current_path` não pôde ser listado
                continue

