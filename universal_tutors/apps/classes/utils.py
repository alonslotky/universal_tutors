import datetime
from django.db.models import Q
from apps.classes.models import Class

def close_classes():
    dt = datetime.datetime.now() - datetime.timedelta(minutes=5)
    date = dt.date()
    time = dt.time()
    
    [class_.done() for class_ in Class.objects.filter(Q(status=Class.STATUS_TYPES.BOOKED), Q(date__lt=date) | Q(date=date, end__lte=time))]
    
def alert_classes():
    dt = datetime.datetime.now() + datetime.timedelta(minutes=30)
    date = dt.date()
    time = dt.time()
    
    [class_.alert() for class_ in Class.objects.filter(Q(status=Class.STATUS_TYPES.BOOKED, alert_sent=False), Q(date__lt=date) | Q(date=date, start__lte=time))]