from django import http
from apps.profile.models import *
from apps.classes.models import *
from apps.core.models import Video, Currency
from apps.core.utils import *

from ordereddict import OrderedDict
import datetime, random, os
import xlwt
import mimetypes

def add_classes_sheet(wbk, classes):
    sheet = wbk.add_sheet('classes')

    sheet.write(0,0, 'Subject')
    sheet.write(0,1, 'Level')
    sheet.write(0,2, 'Educational System')
    sheet.write(0,3, 'Tutor')
    sheet.write(0,4, 'Student')
    sheet.write(0,5, 'Date')
    sheet.write(0,6, 'Duration (min)')
    sheet.write(0,7, 'Credit fee')
    sheet.write(0,8, 'Universal fee')
    sheet.write(0,9, 'Price per hour')
    sheet.write(0,10, 'Status')

    for index, class_ in enumerate(classes.exclude(status__in=[Class.STATUS_TYPES.BOOKED, Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING])):
        sheet.write(index+1, 0, class_.only_subject)
        sheet.write(index+1, 1, class_.level)
        sheet.write(index+1, 2, class_.system)
        sheet.write(index+1, 3, class_.tutor.get_full_name())
        sheet.write(index+1, 4, class_.student.get_full_name())
        sheet.write(index+1, 5, '%s' % class_.date)
        sheet.write(index+1, 6, class_.duration)
        sheet.write(index+1, 7, class_.credit_fee)
        sheet.write(index+1, 8, class_.universal_fee)
        sheet.write(index+1, 9, class_.subject_credits_per_hour)
        sheet.write(index+1, 10, class_.get_status_display())


def get_period(context):
    if context['year']:
        if context['month']:
            if context['day']:
                return '%s %s %s' % (context['year'], context['months'][context['month']][1], context['day'])
            else:
                return '%s %s' % (context['year'], context['months'][context['month']][1])
        else:
            return '%s' % context['year']
    else:
        return 'All time'
    

def get_items(sheet, dtc, title, ordering=False, global_index=0):
    sheet.write(global_index, 0, title)
    sheet.write(global_index, 1, 'Complete')
    sheet.write(global_index, 2, 'Canceled by student')
    sheet.write(global_index, 3, 'Canceled by tutor')
    sheet.write(global_index, 4, 'Canceled by system')
    sheet.write(global_index, 5, 'Rejected by tutor')
    sheet.write(global_index, 6, 'Dropped by student')
     
    global_index += 1
    next_index = global_index
    
    if ordering:
        items = sorted([(key, value) for key, value in dtc.items()], key=lambda x: x[0])
    else:
        items = [(key, value) for key, value in dtc.items()]

    for index, (key, item) in enumerate(items):
        sheet.write(global_index+index, 0, key)
        sheet.write(global_index+index, 1, len(item[Class.STATUS_TYPES.DONE]))
        sheet.write(global_index+index, 2, len(item[Class.STATUS_TYPES.CANCELED_BY_STUDENT]))
        sheet.write(global_index+index, 3, len(item[Class.STATUS_TYPES.CANCELED_BY_TUTOR]))
        sheet.write(global_index+index, 4, len(item[Class.STATUS_TYPES.CANCELED_BY_SYSTEM]))
        sheet.write(global_index+index, 5, len(item[Class.STATUS_TYPES.REJECTED_BY_TUTOR]))
        sheet.write(global_index+index, 6, len(item[Class.STATUS_TYPES.STOPPED_BY_STUDENT]))
        next_index = global_index+index    

    return next_index + 3
    


def reports_students_xls(context):
    period = get_period(context)
    wbk = xlwt.Workbook()
    
    sheet = wbk.add_sheet('general')
    sheet.write(0,0, 'Period')
    sheet.write(0,1, period)

    sheet.write(1,0, 'Total number of students')
    sheet.write(1,1, context['total_students'])
    sheet.write(2,0, 'Number of students who have taking classes')
    sheet.write(2,1, context['students_taking_classes'])
    sheet.write(3,0, 'Number of students that signed up in this period')
    sheet.write(3,1, context['students_signed_up'])

    global_index = get_items(sheet, context['system'], 'Educational system', True, 5)
    global_index = get_items(sheet, context['level'], 'Level', True, global_index)
    global_index = get_items(sheet, context['subject'], 'Subject', True, global_index)
    global_index = get_items(sheet, context['subject_level'], 'Subject and Level', True, global_index)

    add_classes_sheet(wbk, context['classes'])
    
    name = ('students-%s.xls' % ''.join(period.split())).lower()
    filename = os.path.join(settings.SITE_ROOT, 'reports', name)
    wbk.save(filename)
    
    fsock = open(filename, 'r')
    response = http.HttpResponse(fsock, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % name
    return response
        

def reports_tutors_xls(context):
    period = get_period(context)
    wbk = xlwt.Workbook()
    
    sheet = wbk.add_sheet('general')
    sheet.write(0,0, 'Period')
    sheet.write(0,1, period)

    sheet.write(1,0, 'Total number of tutors')
    sheet.write(1,1, context['total_tutors'])
    sheet.write(2,0, 'Number of tutors who have giving classes')
    sheet.write(2,1, context['tutors_taking_classes'])
    sheet.write(3,0, 'Number of tutors that signed up in this period')
    sheet.write(3,1, context['tutors_signed_up'])

    global_index = get_items(sheet, context['system'], 'Educational system', True, 5)
    global_index = get_items(sheet, context['level'], 'Level', True, global_index)
    global_index = get_items(sheet, context['subject'], 'Subject', True, global_index)
    global_index = get_items(sheet, context['subject_level'], 'Subject and Level', True, global_index)

    add_classes_sheet(wbk, context['classes'])
    
    name = ('tutors-%s.xls' % ''.join(period.split())).lower()
    filename = os.path.join(settings.SITE_ROOT, 'reports', name)
    wbk.save(filename)
    
    fsock = open(filename, 'r')
    response = http.HttpResponse(fsock, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % name
    return response


def reports_classes_xls(context):
    period = get_period(context)
    wbk = xlwt.Workbook()
    
    sheet = wbk.add_sheet('general')
    sheet.write(0,0, 'Period')
    sheet.write(0,1, period)

    sheet.write(2, 0, 'Complete')
    sheet.write(3, 0, 'Canceled by student')
    sheet.write(4, 0, 'Canceled by tutor')
    sheet.write(5, 0, 'Canceled by system')
    sheet.write(6, 0, 'Rejected by tutor')
    sheet.write(7, 0, 'Dropped by student')
    sheet.write(2, 1, context['class_status'][Class.STATUS_TYPES.DONE])
    sheet.write(3, 1, context['class_status'][Class.STATUS_TYPES.CANCELED_BY_STUDENT])
    sheet.write(4, 1, context['class_status'][Class.STATUS_TYPES.CANCELED_BY_TUTOR])
    sheet.write(5, 1, context['class_status'][Class.STATUS_TYPES.CANCELED_BY_SYSTEM])
    sheet.write(6, 1, context['class_status'][Class.STATUS_TYPES.REJECTED_BY_TUTOR])
    sheet.write(7, 1, context['class_status'][Class.STATUS_TYPES.STOPPED_BY_STUDENT])

    global_index = get_items(sheet, context['system'], 'Educational system', True, 10)
    global_index = get_items(sheet, context['level'], 'Level', True, global_index)
    global_index = get_items(sheet, context['subject'], 'Subject', True, global_index)
    global_index = get_items(sheet, context['subject_level'], 'Subject and Level', True, global_index)

    add_classes_sheet(wbk, context['classes'])
    
    name = ('classes-%s.xls' % ''.join(period.split())).lower()
    filename = os.path.join(settings.SITE_ROOT, 'reports', name)
    wbk.save(filename)
    
    fsock = open(filename, 'r')
    response = http.HttpResponse(fsock, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % name
    return response


def reports_financial_xls(context):
    period = get_period(context)
    wbk = xlwt.Workbook()
    
    sheet = wbk.add_sheet('general')
    sheet.write(0,0, 'Period')
    sheet.write(0,1, period)
    sheet.write(1,0, 'Unused credits')
    sheet.write(1,1, context['unused_credits'])

    sheet.write(3, 0, 'Type')
    sheet.write(3, 1, 'Credits')
    
    sheet.write(4, 0, 'Top-up')
    sheet.write(4, 1, context['topup_credits'])
    
    sheet.write(5, 0, 'Withdraw')
    sheet.write(5, 1, context['withdraw_credits'])
    
    sheet.write(6, 0, 'Profit')
    sheet.write(6, 1, context['profit_credits'])

    for index, (key, currency) in enumerate(context['currencies'].iteritems()):
        sheet.write(3, 2+index, '%s' % currency['name'])
        sheet.write(4, 2+index, currency['topup'])
        sheet.write(5, 2+index, currency['withdraw'])
        sheet.write(6, 2+index, 'N/A')
        
    sheet.write(8, 0, 'Credits to withdraw')
    sheet.write(8, 1, context['credits_to_withdraw'])
    for index, (key, currency) in enumerate(context['currencies'].iteritems()):
        sheet.write(9+index, 0, 'Value to withdraw in %s' % currency['name'])
        sheet.write(9+index, 1, currency['withdraw'])


    
    name = ('financial-%s.xls' % ''.join(period.split())).lower()
    filename = os.path.join(settings.SITE_ROOT, 'reports', name)
    wbk.save(filename)
    
    fsock = open(filename, 'r')
    response = http.HttpResponse(fsock, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % name
    return response