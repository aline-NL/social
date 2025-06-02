from setuptools import setup, find_packages
import os

# Lista de pacotes do projeto
PACKAGES = find_packages(include=['core', 'atendimento', 'core.*', 'atendimento.*'])

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

# Lê o README.md para a descrição longa
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="social-atendimento",
    version="0.1.0",
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.8',
    author="Sua Empresa",
    author_email="contato@empresa.com",
    description="Sistema de Atendimento Social",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='django social atendimento',
    url="https://github.com/seu-usuario/seu-projeto",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    project_urls={
        'Source': 'https://github.com/seu-usuario/seu-projeto',
        'Bug Reports': 'https://github.com/seu-usuario/seu-projeto/issues',
    },
)
