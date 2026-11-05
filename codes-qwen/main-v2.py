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
        return caminho or 'C:\\Users\\nicol\\nicolegrazzioli\\tapw-av-llm'

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
