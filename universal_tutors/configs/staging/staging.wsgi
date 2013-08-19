import os,sys
import newrelic.agent
newrelic.agent.initialize('/home/rawjam/sites/universal_tutors/repository/newrelic.ini','staging')

# put the Django project on sys.path
sys.path.insert(0,'/home/rawjam/sites/universal_tutors/repository')
sys.path.insert(0,'/home/rawjam/sites/universal_tutors/repository/universal_tutors')
sys.path.insert(0,'/home/rawjam/sites/universal_tutors/repository/django-paypal')

os.environ["DJANGO_SETTINGS_MODULE"] = "universal_tutors.configs.staging.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
