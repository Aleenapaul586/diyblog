import os
import sys

# Add your project directory to the sys.path
path = '/home/Aleenapaul05/diyblog'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'diyblog.settings_production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 