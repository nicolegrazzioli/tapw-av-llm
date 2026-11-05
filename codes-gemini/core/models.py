from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class SafetyLevel(Enum):
    SAFE_TO_DELETE = "Seguro para remover"     # Builds, caches e dependências recriáveis
    NEEDS_ATTENTION = "Requer atenção"         # Ambientes virtuais (.venv), bases locais
    SYSTEM_CRITICAL = "Crítico / Essencial"    # Configurações sensíveis / sistema


@dataclass(frozen=True)
class WasteSignature:
    """Define as características conhecidas de um diretório de descarte/build."""
    name: str
    safety_level: SafetyLevel
    category: str
    description: str


@dataclass(frozen=True)
class WasteReportItem:
    """Resultado diagnóstico de um diretório identificado. Imutável (Read-Only)."""
    folder_path: Path
    size_bytes: int
    signature: WasteSignature
    git_remote_url: Optional[str]
    git_project_root: Optional[Path]

