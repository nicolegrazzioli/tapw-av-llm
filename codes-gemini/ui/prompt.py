import sys
from pathlib import Path

DEFAULT_SCAN_PATH = r"C:\Users\nicol\nicolegrazzioli\tapw-av-llm"


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

