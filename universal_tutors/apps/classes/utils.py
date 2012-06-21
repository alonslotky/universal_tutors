import datetime
from django.db.models import Q
from apps.classes.models import Class

def close_classes():
    """
        Close classes already finished, classes tutors didn't accept or reject and classes tutors didn't appear after 5 min
    """
    
    now = datetime.datetime.now()
    dt30 = now - datetime.timedelta(minutes=35)
    dt60 = now - datetime.timedelta(minutes=65)
    dt90 = now - datetime.timedelta(minutes=95)
    dt120 = now - datetime.timedelta(minutes=125)
    for class_ in Class.objects.filter(
           Q(status=Class.STATUS_TYPES.BOOKED), 
           Q(date__lte=dt30, duration=30) | 
           Q(date__lte=dt60, duration=60) | 
           Q(date__lte=dt90, duration=90) | 
           Q(date__lte=dt120, duration=120)):
        class_.done()
    
    dtw = now + datetime.timedelta(minutes=15)
    for class_ in Class.objects.filter(status=Class.STATUS_TYPES.WAITING, date__lte=dtw):
        class_.canceled_by_system(reason='Tutor did not confirm the class in the required time frame')

    dtt = now - datetime.timedelta(minutes=5)
    for class_ in Class.objects.filter(status=Class.STATUS_TYPES.BOOKED, date__lte=dtt, tutor_appeared=False):
        class_.canceled_by_system(reason='Tutor did not attend the class')

    
def alert_classes():
    dt = datetime.datetime.now() + datetime.timedelta(minutes=30)
    
    for class_ in Class.objects.filter(Q(status=Class.STATUS_TYPES.BOOKED, alert_sent=False), Q(date__lte=dt)):
        class_.alert(use_thread=False)