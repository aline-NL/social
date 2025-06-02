#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    # Configura o caminho base do projeto
    BASE_DIR = Path(__file__).resolve().parent
    
    # Adiciona o diretório raiz ao PYTHONPATH
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))
    
    # Configuração de ambiente
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    
    # Debug de importação
    if os.environ.get('DJANGO_DEBUG_IMPORT', '').lower() == 'true':
        print("\n=== DEBUG: PYTHONPATH ===")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Base directory: {BASE_DIR}")
        print(f"Python path: {sys.path}")
        
        try:
            import django
            print(f"\nDjango version: {django.__version__}")
            print(f"Django settings: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
            
            # Tenta importar o módulo de configurações
            try:
                from django.conf import settings
                print(f"INSTALLED_APPS: {settings.INSTALLED_APPS}")
            except Exception as e:
                print(f"Error importing settings: {e}")
                
        except ImportError as e:
            print(f"\nError importing Django: {e}")
            return
            
        print("\n=== Directory contents ===")
        for item in os.listdir('.'):
            print(f"- {item}")
            
        if os.path.exists('core'):
            print("\n=== Core directory contents ===")
            for item in os.listdir('core'):
                print(f"- {item}")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Executa o comando
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
