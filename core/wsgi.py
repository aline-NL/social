"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Adiciona o diretório do projeto ao PYTHONPATH
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Configura o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Debug de importação
if os.environ.get('DJANGO_DEBUG_IMPORT', '').lower() == 'true':
    print("\n=== WSGI STARTUP DEBUGGING ===")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Base directory: {BASE_DIR}")
    print(f"Python path: {sys.path}")
    print(f"Script path: {os.path.abspath(__file__)}")
    print("\n=== Directory contents ===")
    for item in os.listdir('.'):
        print(f"- {item}")
    print("\n=== Core directory contents ===")
    if os.path.exists('core'):
        for item in os.listdir('core'):
            print(f"- {item}")

# Imprime informações de depuração adicionais
if DEBUG_IMPORT:
    print("\n=== FINAL PYTHONPATH ===")
    for i, path in enumerate(sys.path):
        print(f"{i}: {path}")
    
    print("\n=== CURRENT DIRECTORY CONTENTS ===")
    try:
        for item in os.listdir('.'):
            print(f"- {item} (dir)" if os.path.isdir(item) else f"- {item}")
    except Exception as e:
        print(f"Error listing directory: {e}")
    
    print("\n=== ATTEMPTING TO IMPORT DJANGO ===")

# Tenta importar o Django para verificar se está disponível
try:
    import django
    if DEBUG_IMPORT:
        print(f"Django version: {django.__version__}")
        print(f"Django path: {os.path.dirname(django.__file__)}")
except ImportError as e:
    if DEBUG_IMPORT:
        print(f"Error importing Django: {e}")
        print("\n=== PYTHON MODULE SEARCH PATH ===")
        for path in sys.path:
            print(f"- {path}")
        print("\n")
    raise

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_prod')

if DEBUG_IMPORT:
    print("\n=== DJANGO SETTINGS ===")
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    
    # Tenta importar as configurações
    try:
        from django.conf import settings
        print(f"INSTALLED_APPS: {settings.INSTALLED_APPS}")
    except Exception as e:
        print(f"Error importing settings: {e}")
        print("\n=== TRACEBACK ===")
        traceback.print_exc()

# Importa e configura a aplicação WSGI do Django
try:
    if DEBUG_IMPORT:
        print("\n=== CREATING WSGI APPLICATION ===")
    
    # Importa a configuração do WhiteNoise personalizada
    from core.whitenoise import get_wsgi_application_with_whitenoise
    
    # Obtém a aplicação WSGI com WhiteNoise configurado
    application = get_wsgi_application_with_whitenoise()
    
    if DEBUG_IMPORT:
        print("WSGI application with WhiteNoise configured successfully!")
except Exception as e:
    if DEBUG_IMPORT:
        print(f"\n=== ERROR CREATING WSGI APPLICATION ===")
        print(f"Error: {e}")
        print("\n=== TRACEBACK ===")
        traceback.print_exc()
        print("\n=== SYS.PATH ===")
        for i, path in enumerate(sys.path):
            print(f"{i}: {path}")
        print("\n")
    raise
