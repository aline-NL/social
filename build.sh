#!/bin/bash

# Exit on error
set -e

# Exibe informações sobre o ambiente
echo "=== Environment Information ==="
python --version
pip --version
node --version
npm --version

# Instala as dependências do Python
echo "=== Installing Python dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

# Executa as migrações do banco de dados
echo "=== Running database migrations ==="
python manage.py migrate --noinput

# Cria um superusuário padrão se não existir (apenas para desenvolvimento)
# Em produção, isso deve ser feito manualmente ou através de variáveis de ambiente
if [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "=== Creating superuser if needed ==="
    python manage.py create_superuser_if_none_exists \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" \
        --password "$DJANGO_SUPERUSER_PASSWORD" || true
fi

# Coleta arquivos estáticos
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

# Verifica se o diretório frontend existe antes de tentar construir
if [ -d "frontend" ]; then
    echo "=== Building frontend ==="
    cd frontend
    
    # Verifica se o package.json existe
    if [ -f "package.json" ]; then
        # Instala as dependências do Node.js
        echo "Installing Node.js dependencies..."
        npm install
        
        # Instala o serve globalmente
        echo "Installing serve globally..."
        npm install -g serve
        
        # Executa o build de produção
        echo "Building frontend for production..."
        npm run build:prod
        
        # Move a pasta dist para o diretório raiz
        echo "Moving build output to frontend-dist..."
        mv dist ../frontend-dist
        
        # Instala o serve no diretório raiz
        echo "Installing serve in root directory..."
        cd ..
        npm install serve --save
    else
        echo "Warning: package.json not found in frontend directory. Skipping frontend build."
    fi
else
    echo "=== Frontend directory not found. Skipping frontend build. ==="
fi

echo "=== Build complete ==="
