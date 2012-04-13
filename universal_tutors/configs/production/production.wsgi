import os, sys

# put the Django project on sys.path
sys.path.append('/home/rawjam/sites/universal_tutors/repository')
sys.path.append('/home/rawjam/sites/universal_tutors/repository/iic')

os.environ["DJANGO_SETTINGS_MODULE"] = "universal_tutors.configs.production.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()