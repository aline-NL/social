# Sistema de Atendimento Social

Sistema de gerenciamento de atendimento social construído com Django (backend) e React (frontend).

## Funcionalidades

- Autenticação de usuários (login/logout)
- Gerenciamento de famílias e membros
- Cadastro de atendimentos
- Relatórios e estatísticas
- Painel administrativo personalizado

## Stack Tecnológica

- **Backend**: Django 4.2
- **Frontend**: React 18 com TypeScript
- **Banco de Dados**: PostgreSQL (Produção), SQLite (Desenvolvimento)
- **Deploy**: Render

## Começando

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL (para produção)

### Configuração do Ambiente de Desenvolvimento

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/social.git
   cd social
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

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

## Solução de Problemas

### Erro: "No module named app"
- Verifique se todos os arquivos `__init__.py` estão presentes
- Confirme se o `PYTHONPATH` está configurado corretamente
- Verifique se o `DJANGO_SETTINGS_MODULE` está apontando para o módulo correto

### Erro ao coletar arquivos estáticos
- Certifique-se de que o `STATIC_ROOT` está configurado corretamente
- Verifique as permissões de escrita no diretório de destino

### Erro de conexão com o banco de dados
- Verifique as credenciais do banco de dados
- Confirme se o banco de dados está acessível a partir do Render

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
