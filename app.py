"""
Arquivo temporário para diagnóstico de importação.
Este arquivo será removido após a resolução do problema.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório do projeto ao PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent
print(f"BASE_DIR: {BASE_DIR}")

# Lista de diretórios no PYTHONPATH
print("\nDiretórios no PYTHONPATH:")
for path in sys.path:
    print(f"- {path}")

# Tenta importar o módulo core
print("\nTentando importar o módulo 'core'...")
try:
    import core
    print("✅ Módulo 'core' importado com sucesso!")
    print(f"Localização do módulo 'core': {os.path.dirname(core.__file__)}")
except ImportError as e:
    print(f"❌ Erro ao importar o módulo 'core': {e}")

# Tenta importar o módulo atendimento
print("\nTentando importar o módulo 'atendimento'...")
try:
    import atendimento
    print("✅ Módulo 'atendimento' importado com sucesso!")
    print(f"Localização do módulo 'atendimento': {os.path.dirname(atendimento.__file__)}")
except ImportError as e:
    print(f"❌ Erro ao importar o módulo 'atendimento': {e}")

print("\nDiagnóstico concluído.")
