import os, sys

# put the Django project on sys.path
sys.path.append('/home/rawjam/sites/universal_tutors/repository')
sys.path.append('/home/rawjam/sites/universal_tutors/repository/universal_tutors')
sys.path.append('/home/rawjam/sites/universal_tutors/repository/paypal')

os.environ["DJANGO_SETTINGS_MODULE"] = "universal_tutors.configs.production.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()