import os, sys

# put the Django project on sys.path
sys.path.insert('/home/rawjam/sites/universal_tutors/repository')
sys.path.insert('/home/rawjam/sites/universal_tutors/repository/universal_tutors')
sys.path.insert('/home/rawjam/sites/universal_tutors/repository/django-paypal')

os.environ["DJANGO_SETTINGS_MODULE"] = "universal_tutors.configs.staging.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()