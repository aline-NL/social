import sys
import django
from django.conf import settings

# Configuração mínima do Django
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django_filters',
    ]
)
django.setup()

# Tenta importar o django_filters
try:
    import django_filters
    print(f"✅ django_filters importado com sucesso de: {django_filters.__file__}")
except ImportError as e:
    print(f"❌ Erro ao importar django_filters: {e}")
    print(f"\nCaminhos de importação do Python:")
    for path in sys.path:
        print(f"  - {path}")
