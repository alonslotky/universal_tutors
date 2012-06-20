import datetime
from django.db.models import Q
from apps.classes.models import Class

def close_classes():
    dt30 = datetime.datetime.now() - datetime.timedelta(minutes=35)
    dt60 = datetime.datetime.now() - datetime.timedelta(minutes=65)
    dt90 = datetime.datetime.now() - datetime.timedelta(minutes=95)
    dt120 = datetime.datetime.now() - datetime.timedelta(minutes=125)
    
    [class_.done() for class_ in Class.objects.filter(Q(status=Class.STATUS_TYPES.BOOKED), Q(date__lte=dt30, duration=30) | Q(date__lte=dt60, duration=60) | Q(date__lte=dt90, duration=90) | Q(date__lte=dt120, duration=120))]
    
    
def alert_classes():
    dt = datetime.datetime.now() + datetime.timedelta(minutes=30)
    
    [class_.alert() for class_ in Class.objects.filter(Q(status=Class.STATUS_TYPES.BOOKED, alert_sent=False), Q(date__lte=dt))]