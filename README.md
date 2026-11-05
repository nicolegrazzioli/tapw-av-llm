# Avaliação e Comparação de Modelos LLM: Gemini vs Qwen

> Avaliar e comparar dois modelos de LLM com um agente de código, sendo um deles o Gemini Flash, e outro a sua escolha no Hugging Face ou nos modelos do Ollama. O outro modelo pode ser rodado localmente ou no Colab.  
> – Defina um contexto de um software simples que você deseja criar.  
> – Colocar os prompts usados em um documento citando os modelos usados, bem como um overview sobre os códigos gerados por cada um.  
> – Ao final, dê a sua avaliação sobre os resultados em ambos os modelos utilizados.

---

## Sumário

- [Contexto de Software](#contexto-de-software)
- [Prompts](#prompts)
- [Gemini 3.8 Flash Medium - Chat Web](#gemini-38-flash-medium---chat-web)
- [Qwen2.5-Coder:7B - Ollama + Colab](#qwen25-coder7b---ollama--colab)

---

## Contexto de Software

Ferramenta utilitária de linha de comando (CLI) para liberar espaço na memória do PC identificando arquivos "lixo" de código

* **Modo 100% Leitura (Read-Only):** Inspeciona e gera relatórios sem alterar, mover ou deletar nenhum arquivo.
* **Caminho Padrão:** Pergunta o diretório inicial no terminal; se o usuário pressionar ENTER, adota um caminho padrão predefinido e lida de forma segura com pastas bloqueadas/sem permissão.
* **Detecção de Lixo Dev:** Identifica diretórios recriáveis de build, caches e dependências (`node_modules`, `target`, `build`, `.venv`, `__pycache__`, etc.).
* **Cálculo de Tamanho:** Calcula recursivamente o tamanho ocupado pelas pastas encontradas.
* **Checagem de Backup Git:** Verifica se o projeto possui `.git` e extrai a URL remota (`origin`) para confirmar se o código está salvo em nuvem.
* **Relatório:** Exibe caminho, tamanho, classificação de segurança (seguro para remoção, necessita atenção ou essencial) e URL do repositório remoto.

---

## Prompts

### PROMPT 1 (Planejamento e Arquitetura)
```text
Atue como um especialista em Arquitetura de Software e Engenharia Python. Quero criar uma ferramenta CLI de diagnóstico e análise de uso de armazenamento em disco. Por favor, NÃO escreva o código ainda; apresente primeiro um Plano de Implementação Detalhado contendo a estrutura modular do programa, a divisão de classes funções e as decisões técnicas que você pretende adotar. 
especificações e limitações:
1. Modo 100% Leitura (RESTRITO): O script é estritamente um diagnosticador. É estritamente proibido alterar, mover ou deletar qualquer arquivo ou pasta (os.remove, shutil.rmtree, etc. são proibidos). 
2. Caminho Inicial: Pergunta o diretório ao iniciar. Se o usuário pressionar ENTER (entrada vazia), adota 'C:\Users\nicol\0-pasta-teste' por padrão. O programa deve lidar de forma transparente com pastas sem permissão de acesso ou arquivos bloqueados, garantindo que a varredura continue sem travar o script. 
3. Varredura de Lixo Dev: Identificar pastas de build dependências recriáveis - ex: dependências de pacotes, caches de ambientes virtuais e compilações (node_modules, target, build, .venv, __pycache__, etc). 
4. Checagem de Backup no Git: Para cada pasta de lixo encontrada, verifica se o projeto pai possui uma pasta .git com a URL do repositório remoto (exibindo a URL para confirmar que o código está a salvo na nuvem). 
5. Relatório Final: para cada pasta, exibe uma lista no terminal com: Caminho da Pasta, Tamanho em MB/GB, Tipo de Lixo (se eh seguro remover, se necessita atençao ou se eh algo essencial ao sistema) e URL do GitHub (se houver). Apresente a arquitetura de funções classes que você pretende adotar.
```

### PROMPT 2 (Primeira Metade do Código)
```text
Com base no plano de implementação que você acabou de propor, escreva agora a primeira metade dos códigos em Python. Comece pelas classes principais e pela lógica de funcionamento (varredura de lixo dev e checagem do .git). Lembre das regras e limitações (modo 100% leitura, sem deletar nada)
```

### PROMPT 3 (Segunda Metade do Código e Integração)
```text
agora faça o restante dos codigos, seguindo o plano de implementaçao, sem quebrar nenhum codigo. lembre de Garantir a implementação da pergunta inicial do diretório no terminal, validando a tecla ENTER para usar o caminho padrão (C:\Users\nicol\0-pasta-teste)
```

> **Qwen (Prompt 4 adicional):** O modelo Qwen gerou um código com erro de execução ao final do Prompt 3 (v1). Foi necessário um 4º prompt com o traceback para que ele gerasse uma versão corrigida (v2).

---

## Gemini 3.8 Flash Medium - Chat Web

O Gemini entregou uma arquitetura modular dividida em pacotes em [`codes-gemini/`](codes-gemini/):

* **`core/models.py` & `rules.py`:** Utiliza `dataclass(frozen=True)` e `Enum` (`SafetyLevel`) para garantir imutabilidade dos dados diagnósticos. Possui catálogo amplo de assinaturas de lixo cobrindo Node.js, Python, Java, Rust e Go.
* **`core/size_calculator.py`:** Algoritmo iterativo com pilha (`stack`) e `os.scandir` para cálculo recursivo de tamanho, evitando estouro de recursão em diretórios profundos e tratando exceções de permissão.
* **`engine/scanner.py`:** Mecanismo de varredura baseado em *Generators* (`yield`), transmitindo resultados sob demanda sem sobrecarregar a memória.
* **`git/inspector.py`:** Sobe a árvore de pastas até a raiz do projeto e lê `.git/config` diretamente, sem depender do comando externo `git`.
* **`ui/prompt.py` & `reporter.py`:** Valida entrada e caminhos com tratamento defensivo (limpeza de aspas e checagem de diretório) e gera saída estruturada com cores ANSI e resumo de espaço ocupado.
* **Resultado:** Funcionou na primeira execução sem erros, cobrindo todos os requisitos ([`output-gemini.md`](codes-gemini/output-gemini.md)).

### respostas prompt 1
```text
1. Visão Geral da Arquitetura & Decisões Técnicas
A ferramenta será projetada seguindo os princípios de Separação de Responsabilidades (SoC) e Design Baseado em Domínio (DDD leve), garantindo desacoplamento entre a leitura do sistema de arquivos, a classificação das regras de negócio e a apresentação no terminal.
┌────────────────────────────────────────────────────────┐
│                   CLI / Orchestrator                   │
└────────────┬──────────────────────────────┬────────────┘
             │                              │
             ▼                              ▼
┌─────────────────────────┐    ┌─────────────────────────┐
│     Scanner Engine      │    │      Git Inspector      │
│ (os.scandir / Read-Only)│    │   (Pure Config Parser)  │
└────────────┬────────────┘    └────────────┬────────────┘
             │                              │
             └──────────────┬───────────────┘
                            ▼
              ┌───────────────────────────┐
              │      Report Presenter     │
              │  (Classificação & Output) │
              └───────────────────────────┘
Decisões de Engenharia
Uso Exclusivo de os.scandir em vez de os.walk ou Path.rglob:
os.scandir consome os metadados do diretório já fornecidos pelo sistema operacional (via FindNextFileW no Windows), evitando chamadas de sistema adicionais (stat()) para determinar se uma entrada é pasta ou arquivo.
follow_symlinks=False será forçado em todas as etapas para evitar loops infinitos em junções do Windows (Directory Junctions) e atalhos circulares.
Poda de Árvore (Pruning Inteligente):
Ao detectar uma pasta de lixo (ex.: node_modules), o scanner não desce recursivamente para inspecionar os filhos dessa pasta em busca de outros lixos; ele apenas invoca a rotina de medição de tamanho e continua navegando nos nós irmãos. Isso reduz drasticamente o tempo de I/O e a profundidade de recursão.
Inspeção Git sem Subprocesso (git.exe):
Para máxima velocidade e zero dependência externa (não assumindo que o binário do Git esteja no PATH), a detecção do repositório remoto será feita inspecionando diretamente o arquivo .git/config utilizando a biblioteca padrão configparser.
Isolamento de Erros por Bloco (Fail-Safe I/O):
Cada operação de entrada/saída estará contida em blocos try/except capturando PermissionError, FileNotFoundError (comum com links simbólicos quebrados) e OSError (arquivos bloqueados por outros processos ou caminhos que excedam MAX_PATH no Windows, prefixados com \\?\ quando necessário). A varredura nunca aborta.
Garantia de Modo 100% Leitura:
Nenhuma importação de métodos destrutivos (shutil.rmtree, os.remove, os.unlink, pathlib.Path.unlink).
As estruturas que representam os resultados serão imutáveis (@dataclass(frozen=True)).
2. Estrutura Modular do Projeto
Plaintext
disk_scanner/
│
├── core/
│   ├── __init__.py
│   ├── models.py             # Enums de classificação e Dataclasses de resultado
│   ├── rules.py              # Catálogo de assinaturas de pastas dev e heurísticas de risco
│   └── size_calculator.py    # Algoritmo de cálculo de bytes resiliente a permissões
│
├── git/
│   ├── __init__.py
│   └── inspector.py          # Localizador de raiz .git e parser de URL remota
│
├── engine/
│   ├── __init__.py
│   └── scanner.py            # Varredura hierárquica e orquestração do pipeline
│
├── ui/
│   ├── __init__.py
│   ├── prompt.py             # Captura do input inicial e fallback de diretório
│   └── reporter.py           # Formatação tabular, unidades MB/GB e cores ANSI
│
└── main.py                   # Ponto de entrada (CLI controller)
3. Modelagem de Dados (core/models.py e core/rules.py)
Tipos de Classificação de Risco
Python
class SafetyLevel(Enum):
    SAFE_TO_DELETE = "Seguro para remover"     # Builds e caches recriáveis automaticamente
    NEEDS_ATTENTION = "Requer atenção"         # Ambientes virtuais (.venv), bancos locais, backups
    SYSTEM_CRITICAL = "Crítico / Essencial"    # Arquivos do sistema ou metadados de IDE com configs únicas
Estrutura Imutável do Diagnóstico
Python
@dataclass(frozen=True)
class WasteReportItem:
    folder_path: Path
    size_bytes: int
    rule_name: str
    safety_level: SafetyLevel
    description: str
    git_remote_url: Optional[str]
    parent_project_path: Optional[Path]
Catálogo de Regras Pré-Configuradas
SAFE_TO_DELETE: node_modules, target, build, dist, __pycache__, .pytest_cache, .gradle, .turbo, .next, coverage, .angular.
NEEDS_ATTENTION: .venv, venv, env, .tox, vendor (dependendo do lockfile), pastas .cache.
SYSTEM_CRITICAL: Marcador preventivo para caso diretórios sensíveis sejam atingidos por engano (ex: subpastas sob AppData, Windows ou .git interno).
4. Divisão de Classes e Funções
ui/prompt.py
get_target_directory() -> Path
Exibe o prompt CLI.
Captura input(). Se for string vazia, adota Path(r"C:\Users\nicol\0-pasta-teste").
Valida se o caminho existe e é um diretório antes de prosseguir; se inválido, alerta e solicita novamente sem quebrar.
core/size_calculator.py
calculate_directory_size(dir_path: Path) -> int
Itera sobre a árvore do diretório usando os.scandir.
Trata PermissionError e OSError individualmente por arquivo/pasta, somando os arquivos acessíveis e ignorando os bloqueados.
Retorna o total acumulado em bytes.
git/inspector.py
class GitInspector
find_project_root(starting_path: Path, max_depth: int = 5) -> Optional[Path]
Sobe a árvore a partir da pasta de lixo até encontrar uma pasta .git (ou atingir a raiz do volume/limite de profundidade).
extract_remote_url(git_dir: Path) -> Optional[str]
Lê o arquivo de texto .git/config via configparser.ConfigParser.
Extrai remote "origin" -> url.
Trata casos de repositórios locais sem remote ou submódulos, retornando None de forma segura.
engine/scanner.py
class WasteScanner
Recebe o catálogo de assinaturas de core/rules.py.
scan(root_path: Path) -> Generator[WasteReportItem, None, None]
Algoritmo de busca em largura/profundidade com os.scandir.
Compara o nome da entrada com a lista de assinaturas conhecidas.
Ao encontrar uma correspondência:
Obtém o tamanho via calculate_directory_size.
Descobre a raiz do projeto e extrai a URL remota via GitInspector.
Empacota em um WasteReportItem e emite via yield.
Pula a descida interna nesta pasta (evita redundância de varredura).
Ao não encontrar: Desce recursivamente caso seja um diretório comum e acessível.
ui/reporter.py
class TerminalReporter
format_size(bytes_total: int) -> str
Converte bytes para MB ou GB dinamicamente com 2 casas decimais.
render_report(items: List[WasteReportItem]) -> None
Exibe uma tabela organizada no terminal com:
Caminho da Pasta (com truncamento visual se necessário ou quebra alinhada).
Tamanho formatado.
Classificação de Risco (destacada por cores ANSI ou rótulos textuais claros: [SEGURO], [ATENÇÃO]).
Status do Git / URL remota (exibe a URL completa ou Sem remoto / Local).
render_summary(items: List[WasteReportItem]) -> None
Exibe métricas agregadas: total de pastas encontradas, espaço total passível de liberação (soma de itens SAFE_TO_DELETE) e itens que exigem atenção.
5. Tratamento de Exceções e Resiliência no Windows
Cenário de Falha
Estratégia de Mitigação
Pasta de Sistema Bloqueada (PermissionError)
O scandir captura o erro no iterador e continua nos nós irmãos adjacentes sem encerrar a execução.
Arquivo Aberto Exclusivamente (EBUSY / OSError: [WinError 32])
Na medição de tamanho, o arquivo específico é registrado como 0 bytes e o restante da pasta continua sendo somado.
Caminhos Extensos (> 260 caracteres)
Normalização de caminhos absolutos com prefixo de namespace estendido \\?\ quando executado em Windows.
Link Simbólico Circular / Junção NTFS
Validação com is_symlink() e desativação estrita de follow_symlinks.
Repositório Git Desconectado / Local
O inspector valida a existência da seção remote "origin"; se ausente, define o campo como "Apenas local (sem backup remoto)".

Validação
Este plano atende integralmente a todas as restrições arquiteturais e de negócio estipuladas. Caso a estrutura modular, o catálogo de regras e as definições de classe estejam alinhados com o que você visualizou, podemos passar para a implementação do código.
```

### respostas prompt 2
```text
Aqui está a primeira metade do sistema, contemplando a modelagem do domínio, o cálculo resiliente de bytes, o inspetor do Git e o motor principal de varredura.

---

### `core/models.py`

```python
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




### `core/rules.py`

```python
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


### `core/size_calculator.py`

```python
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



### `git/inspector.py`

```python
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



### `engine/scanner.py`

```python
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

```

### respostas prompt 3
```text
Aqui está a segunda metade do projeto, concluindo a implementação da ferramenta com o módulo de captura de entrada CLI (ui/prompt.py), o formatador visual do relatório (ui/reporter.py), o ponto de entrada (main.py) e os arquivos de inicialização de pacotes (__init__.py).
ui/prompt.py
Python
import sys
from pathlib import Path

DEFAULT_SCAN_PATH = r"C:\Users\nicol\0-pasta-teste"


def get_target_directory() -> Path:
    """
    Solicita o diretório inicial via terminal.
    Se o usuário pressionar ENTER (entrada vazia), adota DEFAULT_SCAN_PATH.
    Valida a existência do diretório sem travar o script.
    """
    default_path_obj = Path(DEFAULT_SCAN_PATH)

    print("\n" + "=" * 70)
    print("  CLI DISK WASTE & DEV-CLEANUP DIAGNOSTIC TOOL")
    print("  Modo: 100% LEITURA (Nenhum arquivo ou pasta será alterado/apagado)")
    print("=" * 70)

    while True:
        try:
            prompt_label = (
                f"\nInforme o caminho para varredura [Pressione ENTER para '{DEFAULT_SCAN_PATH}']:\n> "
            )
            raw_input = input(prompt_label).strip()

            # Caso 1: Usuário pressionou ENTER -> Usa o caminho padrão
            if not raw_input:
                target_path = default_path_obj
                print(f"[i] Usando caminho padrão: {target_path}")
            else:
                # Remove aspas caso o usuário tenha colado caminho com aspas do Windows
                cleaned_input = raw_input.strip('"').strip("'")
                target_path = Path(cleaned_input)

            # Validação defensiva do caminho
            if not target_path.exists():
                print(f"[!] Erro: O caminho '{target_path}' não foi encontrado no sistema.")
                print("    Por favor, informe um caminho existente ou crie o diretório de teste.")
                continue

            if not target_path.is_dir():
                print(f"[!] Erro: O caminho '{target_path}' é um arquivo, não um diretório.")
                continue

            # Converte para caminho absoluto normalizado
            return target_path.resolve()

        except (KeyboardInterrupt, EOFError):
            print("\n\nOperação cancelada pelo usuário. Encerrando com segurança.")
            sys.exit(0)
ui/reporter.py
Python
from typing import List
from core.models import SafetyLevel, WasteReportItem


class TerminalReporter:
    """
    Formata e exibe os diagnósticos no terminal utilizando 
    tabelas limpas e cores ANSI com suporte ao Windows Terminal/PowerShell.
    """

    # Códigos de cor ANSI
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"

    @staticmethod
    def format_size(bytes_total: int) -> str:
        """Converte bytes para representação legível em MB ou GB com 2 casas decimais."""
        mb = bytes_total / (1024 * 1024)
        if mb >= 1024:
            gb = mb / 1024
            return f"{gb:.2f} GB"
        return f"{mb:.2f} MB"

    @classmethod
    def _get_safety_badge(cls, safety_level: SafetyLevel) -> str:
        """Retorna uma tag visual e colorida correspondente ao nível de risco."""
        if safety_level == SafetyLevel.SAFE_TO_DELETE:
            return f"{cls.GREEN}[SEGURO]{cls.RESET} Seguro para remover"
        if safety_level == SafetyLevel.NEEDS_ATTENTION:
            return f"{cls.YELLOW}[ATENÇÃO]{cls.RESET} Requer atenção (.venv/local)"
        return f"{cls.RED}[CRÍTICO]{cls.RESET} Essencial / Sistema"

    @classmethod
    def render_report(cls, items: List[WasteReportItem]) -> None:
        """Renderiza a lista completa de diretórios descartáveis encontrados."""
        print("\n" + "=" * 90)
        print(f"{cls.BOLD}RELATÓRIO DIAGNÓSTICO DE ARMAZENAMENTO & DEV WASTE{cls.RESET}")
        print("=" * 90)

        if not items:
            print(f"\n{cls.GREEN}✔ Nenhuma pasta de lixo ou build recriável encontrada.{cls.RESET}")
            return

        for idx, item in enumerate(items, start=1):
            formatted_size = cls.format_size(item.size_bytes)
            safety_badge = cls._get_safety_badge(item.signature.safety_level)

            # Identificação do Remote Git
            if item.git_remote_url:
                git_status = f"{cls.CYAN}{item.git_remote_url}{cls.RESET} (Backup na nuvem detectado)"
            elif item.git_project_root:
                git_status = f"{cls.YELLOW}Repositório local (sem remote origin configurado){cls.RESET}"
            else:
                git_status = f"{cls.DIM}Não pertence a um repositório Git{cls.RESET}"

            print(f"\n{cls.BOLD}#{idx:02d} [{item.signature.name}] - {formatted_size}{cls.RESET}")
            print(f"  • {cls.DIM}Caminho:{cls.RESET}       {item.folder_path}")
            print(f"  • {cls.DIM}Classificação:{cls.RESET} {safety_badge}")
            print(f"  • {cls.DIM}Descrição:{cls.RESET}     {item.signature.description}")
            print(f"  • {cls.DIM}Remoto Git:{cls.RESET}    {git_status}")
            print("-" * 90)

    @classmethod
    def render_summary(cls, items: List[WasteReportItem]) -> None:
        """Exibe o balanço final com totalizadores de espaço recuperável."""
        total_items = len(items)
        if total_items == 0:
            return

        total_bytes = sum(item.size_bytes for item in items)
        safe_to_delete_bytes = sum(
            item.size_bytes for item in items if item.signature.safety_level == SafetyLevel.SAFE_TO_DELETE
        )
        attention_bytes = sum(
            item.size_bytes for item in items if item.signature.safety_level == SafetyLevel.NEEDS_ATTENTION
        )
        backed_up_count = sum(1 for item in items if item.git_remote_url is not None)

        print("\n" + f"{cls.BOLD}RESUMO EXECUTIVO DE ESPAÇO:{cls.RESET}")
        print(f"  • Pastas de lixo identificadas:      {cls.BOLD}{total_items}{cls.RESET}")
        print(f"  • Espaço total ocupado por builds:   {cls.BOLD}{cls.format_size(total_bytes)}{cls.RESET}")
        print(f"  • Espaço 100% SEGURO para liberação: {cls.GREEN}{cls.BOLD}{cls.format_size(safe_to_delete_bytes)}{cls.RESET}")
        if attention_bytes > 0:
            print(f"  • Espaço em ambientes de atenção:    {cls.YELLOW}{cls.format_size(attention_bytes)}{cls.RESET}")
        print(f"  • Projetos com backup remoto verificado: {cls.CYAN}{backed_up_count}/{total_items}{cls.RESET}")
        print(f"\n{cls.DIM}[Modo Leitura: Nenhuma exclusão foi realizada no sistema de arquivos]{cls.RESET}\n")
main.py
Python
import sys
import time
from typing import List

from core.models import WasteReportItem
from core.rules import WASTE_SIGNATURES
from engine.scanner import WasteScanner
from ui.prompt import get_target_directory
from ui.reporter import TerminalReporter


def main() -> None:
    # 1. Habilita ANSI escape sequences no terminal do Windows nativo
    if sys.platform.startswith("win"):
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # Habilita ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004) no stdout
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    # 2. Pergunta o diretório inicial com fallback para o default
    target_dir = get_target_directory()

    print(f"\n[~] Iniciando varredura resiliente em: {target_dir}")
    print("[~] Mapeando estruturas e checando repositórios Git (Modo Somente Leitura)...")

    start_time = time.time()
    scanner = WasteScanner(signatures=WASTE_SIGNATURES)
    found_items: List[WasteReportItem] = []

    # 3. Executa a varredura consumindo o generator e imprimindo feedback em tempo real
    try:
        for item in scanner.scan(target_dir):
            found_items.append(item)
            # Feedback discreto durante o scan
            size_str = TerminalReporter.format_size(item.size_bytes)
            print(f"  -> Encontrado: {item.folder_path.name} ({size_str}) em {item.folder_path.parent.name}")
    except KeyboardInterrupt:
        print("\n[!] Varredura interrompida pelo usuário. Apresentando dados coletados até o momento...")

    elapsed = time.time() - start_time
    print(f"[✔] Varredura concluída em {elapsed:.2f} segundos.")

    # 4. Renderiza o relatório completo e o resumo
    TerminalReporter.render_report(found_items)
    TerminalReporter.render_summary(found_items)


if __name__ == "__main__":
    main()
Pacotes de Inicialização (__init__.py)
Para assegurar a importação correta dos módulos, crie os seguintes arquivos vazios (ou com suas respectivas exportações):
core/__init__.py
Python
from core.models import SafetyLevel, WasteReportItem, WasteSignature
from core.rules import WASTE_SIGNATURES
from core.size_calculator import calculate_directory_size

__all__ = [
    "SafetyLevel",
    "WasteReportItem",
    "WasteSignature",
    "WASTE_SIGNATURES",
    "calculate_directory_size",
]
git/__init__.py
Python
from git.inspector import GitInspector

__all__ = ["GitInspector"]
engine/__init__.py
Python
from engine.scanner import WasteScanner

__all__ = ["WasteScanner"]
ui/__init__.py
Python
from ui.prompt import DEFAULT_SCAN_PATH, get_target_directory
from ui.reporter import TerminalReporter

__all__ = ["DEFAULT_SCAN_PATH", "get_target_directory", "TerminalReporter"]
Como Executar
Estando na pasta raiz do projeto (disk_scanner/):
Bash
python main.py

Ao iniciar, pressione apenas ENTER para que o caminho C:\Users\nicol\0-pasta-teste seja selecionado automaticamente.
Caso informe um diretório inexistente, o script alerta sem quebrar e permite corrigir a entrada.
Durante a execução, pastas com permissão negada ou arquivos travados pelo sistema operacional são ignorados de forma resiliente, assegurando 100% de leitura sem nenhuma exclusão de dados.
```

---

## Qwen2.5-Coder:7B - Ollama + Colab

### Versão 1 (v1 - Prompt 3)
A versão gerada pelo Qwen ao concluir o Prompt 3 foi dividida em módulos procedurais em [`codes-qwen/`](codes-qwen/):
* **Lógica:** Funções separadas para varredura com `os.walk` (`directory_traversal.py`), identificação por substrings (`garbage_identification.py`), checagem simples de `.git` no diretório imediato (`backup_check.py`) e cálculo/relatório (`report.py`).
* **Falha de Execução:** Ao executar [`main-v1.py`](codes-qwen/main-v1.py), o programa quebrou com `NameError: name 'get_directory_size' is not defined`. O modelo chamou a função de cálculo de tamanho na linha 25, mas importou apenas `generate_report` de `report.py`, esquecendo de importar `get_directory_size`. O script abortou antes de exibir o relatório ([`output-qwen-v1.txt`](codes-qwen/output-qwen-v1.txt)).

### Versão 2 (v2 - Prompt 4: Correção Adicional)
Com o envio do traceback no Prompt 4, o Qwen reescreveu a solução em um único arquivo orientado a objetos ([`main-v2.py`](codes-qwen/main-v2.py)):
* **Lógica:** Agrupou tudo nas classes `Diagnóstico` (fluxo principal e cálculo interno de tamanho), `Varredura`, `Analise` (classificação e git) e `Relatorio`.
* **Resultado:** Corrigiu o `NameError`, adicionou formatação dinâmica de grandezas (B, KB, MB, GB) e executou com sucesso ([`output-qwen-v2.txt`](codes-qwen/output-qwen-v2.txt)).

### preparação de ambiente
```code
!sudo apt-get install zstd
```

```code
# 1. Instalação do Ollama no ambiente Linux do Colab
!curl -fsSL https://ollama.com/install.sh | sh


# 2. Instalação da biblioteca Python do Ollama
!pip install ollama -q

import subprocess
import time
import ollama

```

```code
# Inicia o daemon do Ollama em segundo plano
process = subprocess.Popen(
    ["ollama", "serve"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)


# Aguarda a inicialização do socket do serviço
time.sleep(4)


# Modelo recomendado para código e arquitetura rápida na T4
MODEL_NAME = "qwen2.5-coder:7b"


print(f"Baixando e carregando o modelo {MODEL_NAME}...")
ollama.pull(MODEL_NAME)
print("Modelo pronto para uso na GPU!")
```

```code
messages_history = []

def send_prompt(prompt_text: str, step_title: str):
    print(f"\n{'='*20} {step_title} {'='*20}\n")
   
    # Adiciona a entrada do usuário ao histórico da conversa
    messages_history.append({"role": "user", "content": prompt_text})
   
    stream = ollama.chat(
        model=MODEL_NAME,
        messages=messages_history,
        stream=True
    )
   
    full_response = ""
    for chunk in stream:
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
        full_response += content
       
    # Salva a resposta do assistente para manter coerência nos próximos prompts
    messages_history.append({"role": "assistant", "content": full_response})
    print("\n")
```

### respostas prompt 1
```text
### Plano de Implementação Detalhado

#### Estrutura Modular do Programa

1. **Main Module**
   - `main.py`: 
     - Recebe o caminho inicial do usuário.
     - Inicia a varredura do diretório.
     - Exibe o relatório final.

2. **Directory Traversal Module**
   - `directory_traversal.py`:
     - Define a função `traverse_directory(path)` para varrer o diretório.
     - Ignora pastas sem permissão de acesso e arquivos bloqueados.

3. **Garbage Identification Module**
   - `garbage_identification.py`:
     - Define a função `identify_garbage(path)` para identificar pastas de build e dependências recriáveis.
     - Cria uma lista de pastas consideradas lixo.

4. **Backup Check Module**
   - `backup_check.py`:
     - Define a função `check_backup(path)` para verificar se há um repositório Git no projeto pai.
     - Exibe a URL do repositório Git (se houver).

5. **Report Module**
   - `report.py`:
     - Define a função `generate_report(garbage_list)` para gerar o relatório final.
     - Exibe informações sobre cada pasta, tamanho, tipo de lixo e URL do repositório Git.

#### Classes e Funções

1. **Main Module**
   - `main.py`:
     ```python
     import os
     from directory_traversal import traverse_directory
     from garbage_identification import identify_garbage
     from backup_check import check_backup
     from report import generate_report

     def main():
         path = input("Digite o caminho inicial (Enter para usar 'C:\\Users\\nicol\\0-pasta-teste'): ")
         if not path:
             path = 'C:\\Users\\nicol\\0-pasta-teste'

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
     ```

2. **Directory Traversal Module**
   - `directory_traversal.py`:
     ```python
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
     ```

3. **Garbage Identification Module**
   - `garbage_identification.py`:
     ```python
     import os

     def identify_garbage(path):
         garbage_patterns = ['node_modules', 'target', 'build', '.venv', '__pycache__']
         for pattern in garbage_patterns:
             if pattern in path:
                 return 'Lixo Seguro'
         return None
     ```

4. **Backup Check Module**
   - `backup_check.py`:
     ```python
     import os

     def check_backup(path):
         git_path = os.path.join(path, '.git')
         if os.path.exists(git_path):
             with open(os.path.join(git_path, 'config'), 'r') as f:
                 for line in f:
                     if 'url' in line:
                         return line.split('=')[1].strip().strip('"')
         return None
     ```

5. **Report Module**
   - `report.py`:
     ```python
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
     ```

#### Decisões Técnicas

1. **Modo 100% Leitura (RESTRITO)**: A função `traverse_directory` ignora pastas sem permissão de acesso e arquivos bloqueados, garantindo que a varredura continue sem travar o script.

2. **Caminho Inicial**: O script pede ao usuário para inserir o caminho inicial. Se o usuário pressionar ENTER, o script usa o caminho padrão 'C:\\Users\\nicol\\0-pasta-teste'.

3. **Varredura de Lixo Dev**: A função `identify_garbage` verifica pastas conhecidas como lixo (como `node_modules`, `target`, `build`, `.venv`, `__pycache__`).

4. **Checagem de Backup no Git**: A função `check_backup` verifica a existência de um repositório Git no projeto pai e retorna a URL do repositório remoto (se houver).

5. **Relatório Final**: A função `generate_report` exibe informações sobre cada pasta, tamanho, tipo de lixo e URL do repositório Git.

Essa estrutura modular e as decisões técnicas propostas garantem que a ferramenta CLI seja eficiente, segura e funcional para o diagnóstico e análise de uso de armazenamento em disco.
```

### respostas prompt 2
```text
Claro, aqui está a primeira metade dos códigos em Python, focando nas classes principais e na lógica de funcionamento para varredura de lixo dev e checagem do `.git`. Vou começar com a definição das classes e das funções chave.

### Main Module
import os
from directory_traversal import traverse_directory
from garbage_identification import identify_garbage
from backup_check import check_backup
from report import generate_report

def main():
    path = input("Digite o caminho inicial (Enter para usar 'C:\\Users\\nicol\\0-pasta-teste'): ")
    if not path:
        path = 'C:\\Users\\nicol\\0-pasta-teste'

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


### Directory Traversal Module
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


### Garbage Identification Module
import os

def identify_garbage(path):
    garbage_patterns = ['node_modules', 'target', 'build', '.venv', '__pycache__']
    for pattern in garbage_patterns:
        if pattern in path:
            return 'Lixo Seguro'
    return None


### Backup Check Module
import os

def check_backup(path):
    git_path = os.path.join(path, '.git')
    if os.path.exists(git_path):
        with open(os.path.join(git_path, 'config'), 'r') as f:
            for line in f:
                if 'url' in line:
                    return line.split('=')[1].strip().strip('"')
    return None


### Report Module
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


### Explicação das Funções e Classes

1. **Main Module**
   - `main.py`: 
     - Solicita ao usuário o caminho inicial.
     - Inicia a varredura do diretório utilizando a função `traverse_directory`.
     - Identifica pastas de lixo usando a função `identify_garbage`.
     - Verifica o repositório Git usando a função `check_backup`.
     - Gera e exibe o relatório final usando a função `generate_report`.

2. **Directory Traversal Module**
   - `directory_traversal.py`:
     - Define a função `traverse_directory` para varrer o diretório de forma segura, ignorando pastas sem permissão de acesso.
     - Define a função `handle_error` para tratar erros durante a varredura.

3. **Garbage Identification Module**
   - `garbage_identification.py`:
     - Define a função `identify_garbage` para identificar pastas conhecidas como lixo (como `node_modules`, `target`, `build`, `.venv`, `__pycache__`).

4. **Backup Check Module**
   - `backup_check.py`:
     - Define a função `check_backup` para verificar a existência de um repositório Git no projeto pai e retornar a URL do repositório remoto (se houver).

5. **Report Module**
   - `report.py`:
     - Define a função `get_directory_size` para calcular o tamanho total de uma pasta em MB.
     - Define a função `generate_report` para exibir informações sobre cada pasta, tamanho, tipo de lixo e URL do repositório Git.

Essa primeira metade das classes e funções fornecem a base para a ferramenta CLI, permitindo a varredura segura de pastas, identificação de lixo, verificação de backup no Git e geração de relatórios. A próxima metade do código, que será implementada posteriormente, poderá focar em adicionar funcionalidades adicionais e melhorias de performance.
```

### respostas prompt 3
```text
Claro! Vamos continuar com a implementação restante dos códigos, garantindo que a ferramenta CLI atenda às especificações e limitações fornecidas. Vou continuar com as classes e funções necessárias.

### Directory Traversal Module
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


### Garbage Identification Module
# garbage_identification.py
import os

def identify_garbage(path):
    garbage_patterns = ['node_modules', 'target', 'build', '.venv', '__pycache__']
    for pattern in garbage_patterns:
        if pattern in path:
            return 'Lixo Seguro'
    return None

### Backup Check Module
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

### Report Module
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


### Main Module
# main.py
import os
from directory_traversal import traverse_directory
from garbage_identification import identify_garbage
from backup_check import check_backup
from report import generate_report

def get_input_path():
    path = input("Digite o caminho inicial (Enter para usar 'C:\\Users\\nicol\\0-pasta-teste'): ")
    if not path:
        path = 'C:\\Users\\nicol\\0-pasta-teste'
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


### Explicação das Funções e Classes

1. **Directory Traversal Module**
   - `directory_traversal.py`:
     - Define a função `traverse_directory` para varrer o diretório de forma segura, ignorando pastas sem permissão de acesso.
     - Define a função `handle_error` para tratar erros durante a varredura.

2. **Garbage Identification Module**
   - `garbage_identification.py`:
     - Define a função `identify_garbage` para identificar pastas conhecidas como lixo (como `node_modules`, `target`, `build`, `.venv`, `__pycache__`).

3. **Backup Check Module**
   - `backup_check.py`:
     - Define a função `check_backup` para verificar a existência de um repositório Git no projeto pai e retornar a URL do repositório remoto (se houver).

4. **Report Module**
   - `report.py`:
     - Define a função `get_directory_size` para calcular o tamanho total de uma pasta em MB.
     - Define a função `generate_report` para exibir informações sobre cada pasta, tamanho, tipo de lixo e URL do repositório Git.

5. **Main Module**
   - `main.py`:
     - Solicita ao usuário o caminho inicial usando a função `get_input_path`.
     - Inicia a varredura do diretório utilizando a função `traverse_directory`.
     - Identifica pastas de lixo usando a função `identify_garbage`.
     - Verifica o repositório Git usando a função `check_backup`.
     - Gera e exibe o relatório final usando a função `generate_report`.

Essa implementação completa garante que a ferramenta CLI funcione conforme solicitado, permitindo a varredura segura de pastas, identificação de lixo, verificação de backup no Git e geração de relatórios.
```

### prompt 4
```
prompt_4 = r"""ao rodar 'python main.py' acusou erro - Mensagem de erro completa (Traceback):
Traceback (most recent call last):
  File "C:\Users\nicol\0-pasta-teste\codes-qwen\main.py", line 33, in <module>
    main()
  File "C:\Users\nicol\0-pasta-teste\codes-qwen\main.py", line 25, in main
    'size': get_directory_size(dir_path),
            ^^^^^^^^^^^^^^^^^^
NameError: name 'get_directory_size' is not defined

identifique, explique e retorne os codigos corrigidos e funcionais"""

send_prompt(prompt_4, "PROMPT 4 - CORREÇÃO DO CÓDIGO")
```

```

==================== PROMPT 4 - CORREÇÃO DO CÓDIGO ====================

A mensagem de erro indica que a função `get_directory_size` não foi definida no código. A função `get_directory_size` foi usada no método `calcular_tamanho` da classe `Diagnóstico`, mas não foi implementada. Vamos implementar a função e corrigir o código.

### Código Python - Parte 2: Implementação Completa

Aqui está o código completo, seguindo o plano de implementação, garantindo que a pergunta inicial do diretório seja realizada no terminal, com a opção de usar o caminho padrão (C:\Users\nicol\0-pasta-teste) ao pressionar a tecla ENTER.

import os
import shutil
from typing import List, Dict

class Diagnóstico:
    def iniciar(self):
        caminho = self.obter_caminho()
        pastas_lixo = self.varrer_diretorio(caminho)
        pastas_analizadas = self.chamar_analise(pastas_lixo)
        self.exibir_relatorio(pastas_analizadas)

    def obter_caminho(self) -> str:
        caminho = input("Digite o caminho inicial (ou ENTER para padrão): ")
        return caminho or 'C:\\Users\\nicol\\0-pasta-teste'

    def varrer_diretorio(self, caminho: str) -> List[str]:
        pastas_lixo = []
        for raiz, dirs, arquivos in os.walk(caminho):
            for dir_name in dirs:
                if dir_name in ('node_modules', 'target', 'build', '.venv', '__pycache__'):
                    pastas_lixo.append(os.path.join(raiz, dir_name))
        return pastas_lixo

    def chamar_analise(self, pastas_lixo: List[str]) -> Dict[str, Dict]:
        analisados = {}
        for pasta in pastas_lixo:
            tipo_lixo = Analise.classificar_pasta(pasta)
            backup_git = Analise.verificar_backup_git(pasta)
            tamanho = self.calcular_tamanho(pasta)
            analisados[pasta] = {
                'Tamanho': tamanho,
                'Tipo Lixo': tipo_lixo,
                'Backup Git': backup_git
            }
        return analisados

    def exibir_relatorio(self, analisados: Dict[str, Dict]):
        relatorio = Relatorio.formata_relatorio(analisados)
        print(relatorio)

    def calcular_tamanho(self, pasta: str) -> str:
        tamanho_bytes = self.get_directory_size(pasta)
        return self.formatar_tamanho(tamanho_bytes)

    @staticmethod
    def get_directory_size(dir_path: str) -> int:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    @staticmethod
    def formatar_tamanho(tamanho_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if tamanho_bytes < 1024:
                return f"{tamanho_bytes:.2f} {unit}"
            tamanho_bytes /= 1024

class Varredura:
    @staticmethod
    def varrer(caminho: str) -> List[str]:
        pastas_lixo = []
        for raiz, dirs, arquivos in os.walk(caminho):
            for dir_name in dirs:
                if dir_name in ('node_modules', 'target', 'build', '.venv', '__pycache__'):
                    pastas_lixo.append(os.path.join(raiz, dir_name))
        return pastas_lixo

class Analise:
    @staticmethod
    def classificar_pasta(pasta: str) -> str:
        if pasta.endswith('.venv'):
            return 'Essencial ao Sistema'
        elif pasta.endswith('node_modules') or pasta.endswith('target') or pasta.endswith('build') or pasta.endswith('__pycache__'):
            return 'Seguro para Remoção'
        else:
            return 'Necessita de Atenção'

    @staticmethod
    def verificar_backup_git(pasta: str) -> str:
        git_path = os.path.join(pasta, '.git')
        if os.path.exists(git_path):
            with open(os.path.join(git_path, 'config'), 'r') as f:
                for line in f:
                    if line.startswith('url'):
                        return line.split('=')[1].strip().strip('"')
        return ''

class Relatorio:
    @staticmethod
    def formata_relatorio(analisados: Dict[str, Dict]) -> str:
        relatorio = "RELATÓRIO DE ANÁLISE\n"
        for pasta, info in analisados.items():
            relatorio += f"Caminho: {pasta}\n"
            relatorio += f"Tamanho: {info['Tamanho']}\n"
            relatorio += f"Tipo de Lixo: {info['Tipo Lixo']}\n"
            relatorio += f"URL do GitHub: {info['Backup Git']}\n\n"
        return relatorio

if __name__ == "__main__":
    diagnóstico = Diagnóstico()
    diagnóstico.iniciar()


### Explicação do Código

1. **Classe `Diagnóstico`:**
   - **`iniciar`:** Método principal que coleta informações do usuário e inicia o diagnóstico.
   - **`obter_caminho`:** Obtém o caminho inicial do usuário, com a opção de usar o caminho padrão (C:\Users\nicol\0-pasta-teste) ao pressionar a tecla ENTER.
   - **`varrer_diretorio`:** Varre o diretório e retorna as pastas de lixo.
   - **`chamar_analise`:** Chama os métodos de análise para cada pasta identificada.
   - **`exibir_relatorio`:** Exibe o relatório final.
   - **`calcular_tamanho`:** Calcula e formata o tamanho das pastas usando a função `get_directory_size`.
   - **`get_directory_size`:** Função estática que calcula o tamanho total de um diretório.

2. **Classe `Varredura`:**
   - **`varrer`:** Varre o diretório e retorna as pastas de lixo.

3. **Classe `Analise`:**
   - **`classificar_pasta`:** Classifica as pastas como seguras para remoção, necessitando de atenção ou essenciais ao sistema.
   - **`verificar_backup_git`:** Verifica a presença de um repositório Git e retorna a URL remota.

4. **Classe `Relatorio`:**
   - **`formata_relatorio`:** Formata e exibe as informações das pastas para exibição.

Este código completo realiza o varredura do diretório especificado ou padrão, analisa as pastas de lixo, calcula seu tamanho e exibe um relatório detalhado. A implementação garante que o programa seja executado no modo 100% leitura, conforme solicitado.
```