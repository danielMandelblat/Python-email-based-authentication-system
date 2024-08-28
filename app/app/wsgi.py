import os

from django.core.wsgi import get_wsgi_application

from engine.models import SiteSettings

SiteSettings.apply_settings()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()
