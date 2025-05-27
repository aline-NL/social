from setuptools import setup, find_packages

setup(
    name="social",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.2.10',
        'gunicorn>=21.2.0',
        'whitenoise>=6.6.0',
        'psycopg2-binary>=2.9.9',
        'python-decouple>=3.8',
        'dj-database-url>=2.0.0',
        'django-cors-headers>=4.3.1',
        'Pillow>=10.2.0',
    ],
)
