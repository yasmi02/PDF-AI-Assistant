"""
WSGI config for pdf_ai_project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdf_ai_project.settings')

application = get_wsgi_application()