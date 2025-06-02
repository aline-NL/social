"""
Ponto de entrada principal para execução do pacote social-atendimento.

Este arquivo permite que o pacote seja executado diretamente com:
    python -m social_atendimento [comando] [opções]
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório do projeto ao PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

def main():
    """Função principal para execução do Django management commands."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. Tem certeza que está instalado e "
            "disponível no seu PYTHONPATH? Você esqueceu de ativar um ambiente virtual?"
        ) from exc
    
    # Executa o comando
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
