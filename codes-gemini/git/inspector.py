import configparser
import os
from pathlib import Path
from typing import Optional, Tuple


class GitInspector:
    """
    Inspeciona estruturas Git usando parsing puro de arquivos texto.
    Não executa subprocessos (git.exe) e opera em modo estrito de leitura.
    """

    @staticmethod
    def find_git_root(start_dir: Path, max_depth: int = 6) -> Optional[Path]:
        """
        Sobe recursivamente os diretórios pais para localizar a raiz do repositório Git.
        """
        current = start_dir.resolve()
        depth = 0

        while depth < max_depth:
            git_marker = current / ".git"
            try:
                # .git pode ser diretório ou arquivo (no caso de worktrees / submodules)
                if git_marker.exists():
                    return current
            except (PermissionError, OSError):
                break

            parent = current.parent
            if parent == current:
                # Chegou na raiz do disco (ex: C:\)
                break
            current = parent
            depth += 1

        return None

    @classmethod
    def get_remote_url(cls, project_root: Path) -> Optional[str]:
        """
        Lê o arquivo .git/config e extrai a URL do remote 'origin'.
        Retorna None caso não exista remote configurado ou em caso de erro de leitura.
        """
        git_dir = project_root / ".git"

        # Suporte a worktrees/submodules onde .git é um arquivo com 'gitdir: ...'
        if git_dir.is_file():
            try:
                content = git_dir.read_text(encoding="utf-8", errors="ignore").strip()
                if content.startswith("gitdir:"):
                    rel_gitdir = content.split("gitdir:", 1)[1].strip()
                    git_dir = (project_root / rel_gitdir).resolve()
            except (OSError, UnicodeDecodeError):
                return None

        config_file = git_dir / "config"
        if not config_file.is_file():
            return None

        parser = configparser.ConfigParser(interpolation=None)
        try:
            parser.read(str(config_file), encoding="utf-8")
        except (configparser.Error, OSError, UnicodeDecodeError):
            return None

        # 1. Procura especificamente pela seção de origin
        origin_section = 'remote "origin"'
        if parser.has_section(origin_section) and parser.has_option(origin_section, "url"):
            return parser.get(origin_section, "url").strip()

        # 2. Fallback: pega o primeiro remote disponível se origin não existir
        for section in parser.sections():
            if section.lower().startswith("remote ") and parser.has_option(section, "url"):
                return parser.get(section, "url").strip()

        return None

    @classmethod
    def inspect_path(cls, path: Path) -> Tuple[Optional[Path], Optional[str]]:
        """
        Resolve a raiz do repositório e a URL remota para um dado diretório.
        """
        git_root = cls.find_git_root(path)
        if not git_root:
            return None, None

        remote_url = cls.get_remote_url(git_root)
        return git_root, remote_url

