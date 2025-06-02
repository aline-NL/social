"""
Configuration for WhiteNoise to serve static files in production.
"""
import os
from whitenoise import WhiteNoise
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# This is needed for WhiteNoise to work correctly with Django
# It should be imported in your wsgi.py file

def get_wsgi_application_with_whitenoise():
    """
    Returns a WSGI application with WhiteNoise configured.
    """
    # Get the Django WSGI application
    django_app = get_wsgi_application()
    
    # Configure WhiteNoise
    white_noise = WhiteNoise(
        django_app,
        root=os.path.join(settings.BASE_DIR, 'staticfiles'),
        prefix='static/',
        max_age=31536000,  # 1 year
    )
    
    # Add additional directories to WhiteNoise if needed
    # white_noise.add_files('/path/to/more/static/files', prefix='more-files/')
    
    # Return the WSGI application with WhiteNoise
    return white_noise
