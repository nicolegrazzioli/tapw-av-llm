from typing import Dict
from core.models import SafetyLevel, WasteSignature


WASTE_SIGNATURES: Dict[str, WasteSignature] = {
    # Node.js / Frontend
    "node_modules": WasteSignature(
        name="node_modules",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Dependencies",
        description="Pacotes e dependências do Node.js (recriável via npm/yarn/pnpm install)",
    ),
    ".next": WasteSignature(
        name=".next",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Build Output",
        description="Build cache do Next.js",
    ),
    ".nuxt": WasteSignature(
        name=".nuxt",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Build Output",
        description="Build cache do Nuxt.js",
    ),
    ".angular": WasteSignature(
        name=".angular",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Build Output",
        description="Cache de compilação do Angular",
    ),

    # Python
    "__pycache__": WasteSignature(
        name="__pycache__",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Bytecode Cache",
        description="Bytecode compilado do Python (.pyc)",
    ),
    ".pytest_cache": WasteSignature(
        name=".pytest_cache",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Test Cache",
        description="Cache de execução de testes do Pytest",
    ),
    ".mypy_cache": WasteSignature(
        name=".mypy_cache",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Typecheck Cache",
        description="Cache de checagem estática do Mypy",
    ),
    ".venv": WasteSignature(
        name=".venv",
        safety_level=SafetyLevel.NEEDS_ATTENTION,
        category="Virtualenv",
        description="Ambiente virtual Python (recriável se houver requirements/poetry/pipfile)",
    ),
    "venv": WasteSignature(
        name="venv",
        safety_level=SafetyLevel.NEEDS_ATTENTION,
        category="Virtualenv",
        description="Ambiente virtual Python padrão",
    ),

    # Rust / Java / Outros Compiladores
    "target": WasteSignature(
        name="target",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Build Output",
        description="Artefatos de compilação (Rust/Cargo ou Maven)",
    ),
    "build": WasteSignature(
        name="build",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Build Output",
        description="Artefatos de build genéricos (Gradle, CMake, Webpack, etc.)",
    ),
    "dist": WasteSignature(
        name="dist",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Distribution Output",
        description="Pacotes compilados para distribuição",
    ),
    ".gradle": WasteSignature(
        name=".gradle",
        safety_level=SafetyLevel.SAFE_TO_DELETE,
        category="Build Cache",
        description="Cache local de compilação do Gradle",
    ),
}

