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

