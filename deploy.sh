#!/bin/bash

# Sair imediatamente se algum comando falhar
set -e

echo "=== Iniciando o processo de deploy ==="

# Configura o ambiente
PYTHONPATH="$PYTHONPATH:$(pwd)"
export PYTHONPATH

# Atualiza o pip
echo "=== Atualizando o pip ==="
python -m pip install --upgrade pip

# Instala as dependências
echo "=== Instalando as dependências ==="
pip install -r requirements.txt

# Aplica as migrações
echo "=== Aplicando migrações do banco de dados ==="
python manage.py migrate --noinput

# Coleta arquivos estáticos
echo "=== Coletando arquivos estáticos ==="
python manage.py collectstatic --noinput --clear

# Cria o superusuário se não existir (opcional, descomente se necessário)
# echo "=== Verificando superusuário ==="
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'senha123')" | python manage.py shell

echo "=== Iniciando o servidor Gunicorn ==="
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --worker-class gthread \
    --threads 2 \
    --log-level=info \
    --access-logfile - \
    --error-logfile -

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "Error: render.yaml not found!"
    exit 1
fi

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo "Render CLI not found. Installing..."
    curl -s https://cli.render.com/install.sh | bash
    
    # Add render to PATH if not already there
    if ! grep -q "render" ~/.bashrc; then
        echo 'export PATH="$HOME/.render/cli/current/render:$PATH"' >> ~/.bashrc
        source ~/.bashrc
    fi
    
    echo "Render CLI installed. Please log in to your Render account."
    render auth login
fi

# Deploy to Render
echo "=== Deploying to Render... ==="
render deploy

echo "=== Deployment complete! ==="
