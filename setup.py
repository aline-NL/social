from setuptools import setup, find_packages

# Lista de pacotes do projeto
PACKAGES = find_packages(exclude=['venv*', 'venv311*', 'frontend*'])

# Dependências necessárias
INSTALL_REQUIRES = [
    'Django>=4.2.10',
    'gunicorn>=21.2.0',
    'whitenoise>=6.6.0',
    'psycopg2-binary>=2.9.9',
    'python-decouple>=3.8',
    'dj-database-url>=2.0.0',
    'django-cors-headers>=4.3.1',
    'Pillow>=10.2.0',
    'djangorestframework>=3.14.0',
    'django-filter>=23.1',
]

setup(
    name="social",
    version="0.1",
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.8',
    author="Sua Empresa",
    author_email="contato@empresa.com",
    description="Sistema de Atendimento Social",
    keywords='django social atendimento',
    url="https://github.com/seu-usuario/seu-projeto",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
