#!/usr/bin/env python
"""
Script para verificar o ambiente e identificar possíveis problemas.
Execute este script para diagnosticar problemas comuns de configuração.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

# Configura o Django antes de importar qualquer outro módulo do projeto
try:
    import os
    import django
    from django.conf import settings
    
    # Configura o módulo de configurações do Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    
    # Configura o Django
    django.setup()
    
    # Verifica se as configurações foram carregadas corretamente
    if not settings.configured:
        print("⚠️  As configurações do Django não foram carregadas corretamente.")
        sys.exit(1)
        
    DJANGO_CONFIGURED = True
except Exception as e:
    print(f"❌ Erro ao configurar o Django: {e}")
    DJANGO_CONFIGURED = False
    # Continua a execução para outras verificações básicas

def print_header(title):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * 80)
    print(f" {title.upper()} ".center(80, '='))
    print("=" * 80)

def check_python_version():
    """Verifica a versão do Python."""
    print_header("Versão do Python")
    print(f"Versão do Python: {platform.python_version()}")
    print(f"Executável: {sys.executable}")
    
    # Verifica se a versão é suportada
    version_info = sys.version_info
    if version_info < (3, 8):
        print("⚠️  Aviso: Versão do Python inferior a 3.8 pode causar problemas.")
    else:
        print("✅ Versão do Python compatível.")

def check_environment_variables():
    """Verifica as variáveis de ambiente essenciais."""
    print_header("Variáveis de Ambiente")
    
    required_vars = [
        'DJANGO_SETTINGS_MODULE',
        'SECRET_KEY',
        'DATABASE_URL',
    ]
    
    all_set = True
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {'*' * 8 + value[-4:] if var == 'SECRET_KEY' else value}")
        else:
            print(f"❌ {var}: Não definida")
            all_set = False
    
    # Verifica variáveis opcionais, mas importantes
    optional_vars = [
        'DEBUG',
        'ALLOWED_HOSTS',
        'STATIC_ROOT',
        'MEDIA_ROOT',
    ]
    
    print("\nVariáveis opcionais:")
    for var in optional_vars:
        value = os.environ.get(var)
        if value is not None:
            print(f"ℹ️  {var}: {value}")
        else:
            print(f"⚠️  {var}: Não definida")
    
    return all_set

def check_directories():
    """Verifica se os diretórios necessários existem e têm permissões corretas."""
    print_header("Verificação de Diretórios")
    
    # Diretórios a verificar
    directories = [
        '.',  # Diretório raiz do projeto
        'core',
        'atendimento',
        'static',
        'media',
    ]
    
    for dir_path in directories:
        path = Path(dir_path)
        if path.exists():
            if os.access(str(path), os.R_OK):
                status = "✅"
                if os.access(str(path), os.W_OK):
                    status += " (leitura/escrita)"
                else:
                    status += " (apenas leitura)"
            else:
                status = "❌ Sem permissão de leitura"
            print(f"{status} {dir_path}")
        else:
            print(f"⚠️  Diretório não encontrado: {dir_path}")

def check_python_path():
    """Verifica o PYTHONPATH e a estrutura de importação."""
    print_header("PYTHONPATH e Estrutura de Importação")
    
    # Mostra o PYTHONPATH atual
    print("PYTHONPATH:")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")
    
    # Tenta importar módulos essenciais
    print("\nVerificando importação de módulos:")
    modules_to_check = [
        'django',
        'rest_framework',
        'core',
        'core.settings',
        'atendimento',
    ]
    
    # Verifica apenas módulos Python básicos se o Django não estiver configurado
    if not DJANGO_CONFIGURED:
        print("⚠️  Django não configurado. Verificando apenas módulos básicos...")
        modules_to_check = [m for m in modules_to_check if m not in ['atendimento.models']]
    
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"✅ {module} importado com sucesso")
        except ImportError as e:
            print(f"❌ Falha ao importar {module}: {e}")
    
    # Tenta importar modelos se o Django estiver configurado
    if DJANGO_CONFIGURED:
        try:
            from atendimento import models
            print("✅ Modelos do Django importados com sucesso")
        except Exception as e:
            print(f"❌ Falha ao importar modelos do Django: {e}")

def check_database_connection():
    """Tenta conectar ao banco de dados."""
    print_header("Conexão com o Banco de Dados")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                print("✅ Conexão com o banco de dados bem-sucedida")
            else:
                print("❌ Não foi possível verificar a conexão com o banco de dados")
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")

def check_static_files():
    """Verifica a configuração de arquivos estáticos."""
    print_header("Arquivos Estáticos")
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles import finders
        
        print(f"STATIC_ROOT: {getattr(settings, 'STATIC_ROOT', 'Não definido')}")
        print(f"STATIC_URL: {getattr(settings, 'STATIC_URL', 'Não definido')}")
        
        # Verifica se o diretório de arquivos estáticos existe
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if static_root and os.path.exists(static_root):
            print(f"✅ Diretório de arquivos estáticos encontrado em: {static_root}")
            
            # Verifica permissões
            if os.access(static_root, os.W_OK):
                print("✅ Permissão de escrita no diretório de arquivos estáticos")
            else:
                print("⚠️  Sem permissão de escrita no diretório de arquivos estáticos")
        else:
            print("⚠️  Diretório de arquivos estáticos não encontrado ou não acessível")
        
        # Tenta encontrar um arquivo estático de exemplo
        test_file = finders.find('admin/css/base.css')
        if test_file:
            print(f"✅ Arquivo estático de exemplo encontrado: {test_file}")
        else:
            print("⚠️  Não foi possível encontrar um arquivo estático de exemplo")
            
    except Exception as e:
        print(f"❌ Erro ao verificar arquivos estáticos: {e}")

def check_django_settings():
    """Verifica as configurações do Django."""
    print_header("Configurações do Django")
    
    try:
        from django.conf import settings
        
        # Configurações importantes para verificar
        important_settings = [
            'DEBUG',
            'ALLOWED_HOSTS',
            'DATABASES',
            'INSTALLED_APPS',
            'MIDDLEWARE',
            'ROOT_URLCONF',
            'TEMPLATES',
            'WSGI_APPLICATION',
        ]
        
        for setting in important_settings:
            try:
                value = getattr(settings, setting, 'Não definido')
                if setting == 'SECRET_KEY' and value != 'Não definido':
                    value = '********' + (value[-4:] if value else '')
                print(f"{setting}: {value}")
            except Exception as e:
                print(f"❌ Erro ao acessar {setting}: {e}")
    
    except Exception as e:
        print(f"❌ Erro ao carregar as configurações do Django: {e}")

def setup_django():
    """Configura o Django para execução fora do contexto normal."""
    try:
        import os
        import django
        from django.conf import settings
        
        # Configura o módulo de configurações do Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        
        # Configura o Django
        django.setup()
        
        # Verifica se as configurações foram carregadas corretamente
        if not settings.configured:
            print("⚠️  As configurações do Django não foram carregadas corretamente.")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Erro ao configurar o Django: {e}")
        return False

def main():
    """Função principal."""
    print_header("Verificação do Ambiente de Desenvolvimento")
    print("Este script verifica o ambiente e identifica possíveis problemas.\n")
    
    # Executa todas as verificações básicas
    check_python_version()
    check_environment_variables()
    check_directories()
    check_python_path()
    
    # Verifica se o Django foi configurado corretamente
    if not DJANGO_CONFIGURED:
        print("\n⚠️  O Django não foi configurado corretamente. Algumas verificações não puderam ser realizadas.")
    else:
        try:
            # Verificações que requerem o Django configurado
            check_django_settings()
            check_database_connection()
            check_static_files()
        except Exception as e:
            print(f"\n⚠️  Erro durante as verificações do Django: {e}")
    
    print_header("Verificação Concluída")
    print("\nDica: Se encontrar problemas, consulte a documentação em README.md")
    print("ou execute com DJANGO_DEBUG_IMPORT=true para mais detalhes de depuração.")

if __name__ == "__main__":
    main()
