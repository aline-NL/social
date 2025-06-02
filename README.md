# Sistema de Atendimento Social

Sistema de gerenciamento de atendimento social construído com Django (backend) e React (frontend).

## 🚀 Funcionalidades

- **Autenticação de usuários** com diferentes níveis de acesso (admin, atendente, visualizador)
- **Gerenciamento de famílias e membros** com histórico completo
- **Controle de presença** em encontros e atividades
- **Entrega de cestas básicas** com registro detalhado
- **Relatórios e estatísticas** para análise de dados
- **Painel administrativo** personalizado e intuitivo

## 🛠️ Stack Tecnológica

- **Backend**: Django 4.2 com Django REST Framework
- **Frontend**: React 18 com TypeScript e Vite
- **Banco de Dados**: PostgreSQL (Produção), SQLite (Desenvolvimento)
- **Autenticação**: Sessão do Django
- **Estilização**: Tailwind CSS com design responsivo
- **Deploy**: Render (Full Stack)
- **CI/CD**: GitHub Actions

## 🚀 Deploy no Render (Atualizado)

### Pré-requisitos

- Conta no [Render](https://render.com/)
- Conta no [GitHub](https://github.com/)
- Repositório do projeto no GitHub

### Passo a Passo

1. **Fazer fork do repositório**
   - Acesse o repositório do projeto
   - Clique em "Fork" no canto superior direito

2. **Criar um novo serviço no Render**
   - Acesse o [Painel do Render](https://dashboard.render.com/)
   - Clique em "New" e selecione "Web Service"
   - Conecte sua conta do GitHub
   - Selecione o repositório forkado

3. **Configurar o serviço de backend**
   - Nome: `social-backend`
   - Branch: `main`
   - Build Command: 
     ```bash
     python -m pip install --upgrade pip
     pip install -r requirements.txt
     python manage.py migrate
     python manage.py collectstatic --noinput
     ./frontend/build.sh
     ```
   - Start Command: `gunicorn core.wsgi:application --log-file -`
   - Environment Variables:
     - `DEBUG`: `False`
     - `SECRET_KEY`: Sua chave secreta do Django
     - `ALLOWED_HOSTS`: `.onrender.com`
     - `DATABASE_URL`: URL do seu banco de dados PostgreSQL
     - `CORS_ALLOWED_ORIGINS`: `https://social-frontend.onrender.com`
     - `CSRF_TRUSTED_ORIGINS`: `https://social-backend.onrender.com,https://social-frontend.onrender.com`
     - `STATIC_URL`: `/static/`
     - `STATIC_ROOT`: `staticfiles`
     - `MEDIA_URL`: `/media/`
     - `MEDIA_ROOT`: `media`

4. **Configurar o serviço de frontend**
   - No painel do Render, clique em "New" e selecione "Static Site"
   - Nome: `social-frontend`
   - Branch: `main`
   - Build Command:
     ```bash
     cd frontend
     npm install
     npm run build:prod
     ```
   - Publish Directory: `frontend/dist`
   - Environment Variables:
     - `VITE_API_URL`: `https://social-backend.onrender.com/api`
     python manage.py collectstatic --noinput
     ```
   - Start Command: 
     ```bash
     gunicorn -c gunicorn_config.py core.wsgi:application
     ```

4. **Configurar variáveis de ambiente**
   - `PYTHON_VERSION`: `3.11.0`
   - `DJANGO_SETTINGS_MODULE`: `core.settings_prod`
   - `SECRET_KEY`: Gere uma chave segura
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `social-backend.onrender.com,localhost,127.0.0.1`
   - `CORS_ALLOWED_ORIGINS`: `https://social-frontend.onrender.com,http://localhost:3000`
   - `DATABASE_URL`: Será configurado automaticamente pelo Render

5. **Criar o banco de dados**
   - No painel do Render, clique em "New" e selecione "PostgreSQL"
   - Nome: `social-db`
   - Database: `social`
   - Usuário: `social_user`
   - Plano: Free
   - Região: São Paulo (ou a mais próxima de você)

6. **Configurar o frontend**
   - No painel do Render, clique em "New" e selecione "Static Site"
   - Nome: `social-frontend`
   - Branch: `main`
   - Pasta raiz: `frontend`
   - Comando de build: 
     ```bash
     cd frontend
     npm install
     npm run build:prod
     ```
   - Pasta de saída: `dist`
   - Variáveis de ambiente:
     - `VITE_API_URL`: `https://social-backend.onrender.com/api`
     - `NODE_ENV`: `production`

7. **Configurar domínios personalizados (opcional)**
   - No painel do serviço, vá em "Settings" > "Custom Domains"
   - Adicione seu domínio personalizado
   - Siga as instruções para configurar o DNS

8. **Configurar HTTPS**
   - O Render fornece certificados SSL gratuitos automaticamente
   - Certifique-se de que "Auto-Deploy" está ativado nas configurações do serviço

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Django
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://usuario:senha@localhost:5432/social

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Media files
MEDIA_URL=/media/
MEDIA_ROOT=media

# Static files
STATIC_URL=/static/
STATIC_ROOT=staticfiles
```

### Desenvolvimento Local

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/seu-usuario/social.git
   cd social
   ```

2. **Configurar ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   .\venv\Scripts\activate  # Windows
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar banco de dados**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Iniciar servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```

6. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

7. **Acessar**
   - Backend: http://localhost:8000/admin
   - Frontend: http://localhost:3000

### Docker (Opcional)

```bash
# Construir e iniciar os contêineres
docker-compose up --build

# Executar migrações
docker-compose exec backend python manage.py migrate

# Criar superusuário
docker-compose exec backend python manage.py createsuperuser
```

## 📄 Licença

Este projeto está licenciado sob a licença MIT.

## 🚀 Começando

### 📋 Pré-requisitos

- Python 3.11+
- Node.js 18+ (apenas para desenvolvimento frontend)
- PostgreSQL 13+ (para produção)
- Git

### 🔧 Configuração do Ambiente de Desenvolvimento

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/social.git
   cd social
   ```

2. **Crie e ative um ambiente virtual**
   ```bash
   # Linux/MacOS
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   # python -m venv venv
   # .\venv\Scripts\activate
   ```

3. **Instale as dependências do Python**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```
   
   Exemplo de configuração básica do `.env`:
   ```env
   # Configurações básicas
   DEBUG=True
   SECRET_KEY=sua_chave_secreta_aqui
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Banco de dados (SQLite para desenvolvimento)
   DATABASE_URL=sqlite:///db.sqlite3
   
   # Configurações de e-mail (opcional para desenvolvimento)
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   DEFAULT_FROM_EMAIL=webmaster@localhost
   ```

5. **Aplique as migrações**
   ```bash
   python manage.py migrate
   ```

6. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```

7. **Inicie o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```

8. **Acesse o painel administrativo**
   Abra o navegador em http://localhost:8000/admin/

5. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

6. Crie um superusuário (opcional):
   ```bash
   python manage.py createsuperuser
   ```

7. Execute o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Implantação no Render

### Pré-requisitos

- Conta no [Render](https://render.com/)
- Repositório Git configurado (GitHub, GitLab ou Bitbucket)
- Banco de dados PostgreSQL configurado

### Passo a Passo

1. **Prepare seu repositório**
   - Certifique-se de que todos os arquivos necessários estão commitados
   - Verifique se o `requirements.txt` está atualizado

2. **Crie um novo serviço Web no Render**
   - Acesse o [painel do Render](https://dashboard.render.com/)
   - Clique em "New" e selecione "Web Service"
   - Conecte seu repositório

3. **Configure as variáveis de ambiente**
   - Adicione as seguintes variáveis de ambiente no painel do Render:
     ```
     PYTHON_VERSION=3.11.0
     DJANGO_SETTINGS_MODULE=core.settings
     SECRET_KEY=sua_chave_secreta_aqui
     DEBUG=False
     DISABLE_COLLECTSTATIC=1
     DATABASE_URL=sua_url_do_postgresql_aqui
     ALLOWED_HOSTS=seu-app.onrender.com
     CORS_ALLOWED_ORIGINS=https://seu-frontend.onrender.com
     CSRF_TRUSTED_ORIGINS=https://seu-app.onrender.com
     ```

4. **Configure o comando de build**
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

5. **Configure o comando de inicialização**
   ```
   gunicorn core.wsgi:application --workers 4 --worker-class gthread --threads 2 --log-level=info
   ```

6. **Selecione o plano**
   - Escolha o plano gratuito para começar

7. **Implante**
   - Clique em "Create Web Service"

## 🔧 Solução de Problemas

### Erro: "No module named app"

Este erro geralmente ocorre quando o Python não consegue encontrar os módulos do seu projeto. Aqui estão as etapas para resolver:

1. **Verifique a estrutura de diretórios**
   - Certifique-se de que todos os diretórios do seu projeto contêm um arquivo `__init__.py`
   - A estrutura deve ser algo como:
     ```
     seu_projeto/
     ├── manage.py
     ├── core/
     │   ├── __init__.py
     │   ├── settings.py
     │   ├── urls.py
     │   └── wsgi.py
     └── atendimento/
         ├── __init__.py
         ├── admin.py
         ├── apps.py
         ├── models.py
         ├── urls.py
         └── views.py
     ```

2. **Verifique o PYTHONPATH**
   - Certifique-se de que o diretório raiz do projeto está no `PYTHONPATH`
   - Você pode verificar o `PYTHONPATH` executando:
     ```bash
     python -c "import sys; print('\n'.join(sys.path))"
     ```

3. **Verifique o DJANGO_SETTINGS_MODULE**
   - Certifique-se de que a variável de ambiente `DJANGO_SETTINGS_MODULE` está configurada corretamente
   - Deve ser algo como `core.settings`

4. **Ative o modo de depuração**
   - Adicione `DJANGO_DEBUG_IMPORT=true` às suas variáveis de ambiente
   - Isso ativará mensagens de depuração detalhadas durante a inicialização

### Erro ao coletar arquivos estáticos

1. **Verifique as configurações**
   - Certifique-se de que `STATIC_ROOT` está configurado no seu `settings.py`
   - Exemplo: `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')`

2. **Permissões de diretório**
   - Certifique-se de que o usuário que executa o aplicativo tem permissão para gravar no diretório `STATIC_ROOT`
   - No Linux/Mac: `chmod -R 755 /caminho/para/staticfiles`
   - No Windows: Verifique as permissões de gravação na pasta

3. **Configuração do WhiteNoise**
   - Se estiver usando WhiteNoise, certifique-se de que está configurado corretamente:
     ```python
     MIDDLEWARE = [
         # ...
         'whitenoise.middleware.WhiteNoiseMiddleware',
         # ...
     ]
     
     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
     ```

### Erro de conexão com o banco de dados

1. **Verifique as credenciais**
   - Confirme se as credenciais do banco de dados no seu `.env` estão corretas
   - Exemplo para PostgreSQL:
     ```
     DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
     ```

2. **Verifique a acessibilidade do banco de dados**
   - Tente conectar ao banco de dados manualmente usando as mesmas credenciais
   - Para PostgreSQL: `psql -h localhost -U usuario -d nome_do_banco`

3. **Verifique as migrações pendentes**
   - Execute `python manage.py showmigrations` para verificar se há migrações pendentes
   - Aplique as migrações com `python manage.py migrate`

### Erro durante o deploy no Render

1. **Verifique os logs**
   - Acesse o painel do Render e verifique os logs de build e runtime
   - Procure por mensagens de erro específicas

2. **Verifique as variáveis de ambiente**
   - Certifique-se de que todas as variáveis de ambiente necessárias estão configuradas no painel do Render
   - Inclua `PYTHON_VERSION=3.11.0` nas variáveis de ambiente

3. **Verifique o arquivo `requirements.txt`**
   - Certifique-se de que todas as dependências estão listadas corretamente
   - Tente instalar localmente para ver se há conflitos:
     ```bash
     pip install -r requirements.txt
     ```

## 🐛 Depuração Avançada

### Script de Verificação de Ambiente

O projeto inclui um script `check_environment.py` que verifica automaticamente o ambiente e identifica possíveis problemas. Para usá-lo:

```bash
# Torne o script executável (apenas na primeira vez)
chmod +x check_environment.py

# Execute o script
python check_environment.py
```

O script verificará:
- Versão do Python e ambiente
- Variáveis de ambiente essenciais
- Estrutura de diretórios e permissões
- Configurações do Django
- Conexão com o banco de dados
- Configuração de arquivos estáticos

### Ativando o modo de depuração de importação

Para obter informações detalhadas sobre problemas de importação, defina a variável de ambiente:

```bash
export DJANGO_DEBUG_IMPORT=true  # Linux/Mac
# ou
set DJANGO_DEBUG_IMPORT=true    # Windows
```

### Verificando o ambiente Python

Para verificar se todas as dependências estão instaladas corretamente:

```bash
# Verifique a versão do Python
python --version

# Verifique as dependências instaladas
pip list

# Verifique se o Django está instalado corretamente
python -c "import django; print(django.__version__)"
```

### Testando a aplicação localmente

Antes de fazer o deploy, teste localmente em um ambiente semelhante ao de produção:

```bash
# Instale as dependências de produção
pip install -r requirements.txt

# Configure as variáveis de ambiente de produção
cp .env.example .env.prod
# Edite o .env.prod com as configurações de produção

# Execute com as configurações de produção
export DJANGO_SETTINGS_MODULE=core.settings
export DJANGO_READ_DOT_ENV_FILE=true
python manage.py check --deploy
python manage.py collectstatic --noinput
python manage.py runserver
```

## Suporte

Para suporte, entre em contato com nossa equipe através do email suporte@empresa.com.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Deployment

The application is configured for deployment on Render. The `render.yaml` file contains the configuration for both frontend and backend services.

## Environment Variables

### Backend

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection URL
- `ALLOWED_HOSTS`: List of allowed hosts
- `CORS_ALLOWED_ORIGINS`: List of allowed origins for CORS

### Frontend

- `VITE_API_URL`: Backend API URL

## License

MIT
