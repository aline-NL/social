# Guia de Deploy

Este guia detalha como implantar a aplicação em diferentes ambientes.

## 🚀 Deploy no Render.com

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

3. **Configurar o serviço backend**
   - Nome: `social-backend`
   - Branch: `main`
   - Build Command: 
     ```bash
     python -m pip install --upgrade pip
     pip install -r requirements.txt
     python manage.py migrate
     python manage.py collectstatic --noinput
     ```
   - Start Command: 
     ```bash
     gunicorn -c gunicorn_config.py core.wsgi:application
     ```
   - Environment Variables:
     - `PYTHON_VERSION`: `3.11.0`
     - `PYTHONPATH`: `/opt/render/project/src`
     - `DJANGO_SETTINGS_MODULE`: `core.settings_prod`
     - `SECRET_KEY`: Gere uma chave segura
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `social-backend.onrender.com,localhost,127.0.0.1`
     - `CORS_ALLOWED_ORIGINS`: `https://social-frontend.onrender.com,http://localhost:3000`
     - `CSRF_TRUSTED_ORIGINS`: `https://social-backend.onrender.com,https://social-frontend.onrender.com`
     - `DISABLE_COLLECTSTATIC`: `1`
     - `DATABASE_URL`: Será configurado automaticamente

4. **Criar o banco de dados**
   - No painel do Render, clique em "New" e selecione "PostgreSQL"
   - Nome: `social-db`
   - Database: `social`
   - Usuário: `social_user`
   - Plano: Free
   - Região: São Paulo (ou a mais próxima de você)

5. **Configurar o frontend**
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
   - Environment Variables:
     - `NODE_VERSION`: `18.16.0`
     - `NODE_ENV`: `production`
     - `VITE_API_URL`: `https://social-backend.onrender.com`
     - `CI`: `false`

6. **Configurar domínios personalizados (opcional)**
   - No painel do serviço, vá em "Settings" > "Custom Domains"
   - Adicione seu domínio personalizado
   - Siga as instruções para configurar o DNS

7. **Configurar HTTPS**
   - O Render fornece certificados SSL gratuitos automaticamente
   - Certifique-se de que "Auto-Deploy" está ativado nas configurações do serviço

## 🐳 Desenvolvimento Local com Docker

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/seu-usuario/social.git
   cd social
   ```

2. **Criar e configurar o arquivo .env**
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` com suas configurações locais.

3. **Iniciar os contêineres**
   ```bash
   docker-compose up --build
   ```

4. **Executar migrações**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

5. **Criar superusuário**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

6. **Acessar a aplicação**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin

## 🔄 CI/CD com GitHub Actions

O projeto inclui um workflow do GitHub Actions para testes automatizados e deploy contínuo. O arquivo está localizado em `.github/workflows/deploy.yml`.

### Fluxo de trabalho

1. **Testes**
   - Executa testes do backend e frontend em cada push para a branch `main`
   - Verifica a formatação do código
   - Executa verificações de segurança

2. **Deploy**
   - Implanta automaticamente para o Render quando um novo push é feito na branch `main`
   - Executa migrações do banco de dados
   - Coleta arquivos estáticos

## 🔒 Variáveis de Ambiente

### Backend

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DEBUG` | Modo de depuração | `False` em produção |
| `SECRET_KEY` | Chave secreta do Django | Gere uma chave segura |
| `DATABASE_URL` | URL de conexão com o banco de dados | `postgresql://user:pass@localhost:5432/db` |
| `ALLOWED_HOSTS` | Hosts permitidos | `example.com,localhost` |
| `CORS_ALLOWED_ORIGINS` | Origens permitidas para CORS | `https://frontend.com,http://localhost:3000` |
| `CSRF_TRUSTED_ORIGINS` | Origens confiáveis para CSRF | `https://backend.com,https://frontend.com` |

### Frontend

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `VITE_API_URL` | URL da API do backend | `https://api.example.com` |
| `NODE_ENV` | Ambiente Node.js | `production` |

## 📦 Estrutura do Projeto

```
.
├── .github/                   # Configurações do GitHub
│   └── workflows/             # Workflows do GitHub Actions
├── backend/                   # Código-fonte do backend
│   ├── core/                  # Configurações do projeto Django
│   ├── atendimento/           # Aplicativo principal
│   ├── manage.py
│   └── requirements.txt
├── frontend/                  # Código-fonte do frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── nginx/                     # Configurações do Nginx
│   └── nginx.conf
├── .env.example               # Exemplo de variáveis de ambiente
├── docker-compose.yml         # Configuração do Docker Compose
├── Dockerfile                 # Dockerfile do backend
├── gunicorn_config.py         # Configuração do Gunicorn
└── render.yaml                # Configuração do Render.com
```

## 🔧 Solução de Problemas

### Problemas comuns e soluções

1. **Erro 500 no backend**
   - Verifique os logs do servidor no painel do Render
   - Certifique-se de que todas as migrações foram aplicadas
   - Verifique se as variáveis de ambiente estão configuradas corretamente

2. **CORS errors no frontend**
   - Verifique se o `CORS_ALLOWED_ORIGINS` inclui a URL do frontend
   - Certifique-se de que o backend está retornando os cabeçalhos CORS corretos

3. **Arquivos estáticos não carregando**
   - Execute `python manage.py collectstatic` localmente
   - Verifique se o WhiteNoise está configurado corretamente
   - Certifique-se de que o `STATIC_ROOT` está apontando para o diretório correto

4. **Problemas com o banco de dados**
   - Verifique se a string de conexão do banco de dados está correta
   - Certifique-se de que o banco de dados está acessível a partir do servidor de aplicação
   - Execute as migrações manualmente se necessário

5. **Erros durante o build**
   - Verifique os logs de build no painel do Render
   - Certifique-se de que todas as dependências estão listadas corretamente
   - Tente limpar o cache de build no Render

## 📞 Suporte

Em caso de problemas, abra uma issue no repositório do projeto ou entre em contato com a equipe de desenvolvimento.
