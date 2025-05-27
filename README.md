# Social Network

A social networking platform built with Django (backend) and React (frontend).

## Features

- User authentication (login/register)
- Profile management
- Image uploads
- Posts and comments
- Like and follow functionality

## Tech Stack

- **Backend**: Django 4.2
- **Frontend**: React 18 with TypeScript
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Deployment**: Render

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (for production)

### Backend Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

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
