"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório do projeto ao PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Adiciona o diretório do projeto ao PYTHONPATH (caminho alternativo)
project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.append(project_path)

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Importa e configura a aplicação ASGI do Django
from django.core.asgi import get_asgi_application

# Cria a aplicação ASGI
application = get_asgi_application()
