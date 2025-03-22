import os
import subprocess
import sys
from pathlib import Path

def setup_environment():
    # Definir diretório do projeto
    project_dir = Path('/home/dudu/lista_compras')
    venv_dir = project_dir / 'venv'

    try:
        # Criar ambiente virtual
        print("Criando ambiente virtual...")
        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)

        # Ativar ambiente virtual e instalar dependências
        pip_path = venv_dir / 'bin' / 'pip'
        print("Instalando dependências...")
        subprocess.run([str(pip_path), 'install', 'flask'], check=True)
        subprocess.run([str(pip_path), 'install', 'pandas'], check=True)
        subprocess.run([str(pip_path), 'install', 'fpdf'], check=True)

        print("\nConfiguração concluída com sucesso!")
        print("\nPara ativar o ambiente virtual, use:")
        print("source venv/bin/activate")
        print("\nPara rodar o aplicativo:")
        print("python app.py")

    except subprocess.CalledProcessError as e:
        print(f"Erro durante a instalação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_environment()
