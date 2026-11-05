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

