import datetime, pytz

def first_day_of_week(date):
    return date - datetime.timedelta(days=date.weekday())

def next_month(date):
    year = date.year
    month = date.month
    day = date.day
    
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
        
    while True:
        try:
            return datetime.date(year, month, day)
        except ValueError:
            day -= 1

def prev_month(date):
    year = date.year
    month = date.month
    day = date.day
    
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
        
    while True:
        try:
            return datetime.date(year, month, day)
        except ValueError:
            day -= 1
        

def to_calendar(year, month = None):
    """
    Return a calendar list represented by:
    
    ["first_day_of_mount",[
        ["monday_date", "tuesday_date", ..., "sunday_date"] 
        ["monday_date", "tuesday_date", ..., "sunday_date"] 
        ...
        ["monday_date", "tuesday_date", ..., "sunday_date"] 
    ]]
    """

    try:
        date = datetime.date(year, month, 1)
    except TypeError:
        date = datetime.date(year.year, year.month, 1)

    calendar = [date]
    weeks = []
    
    day = date
    weekday = day.weekday()
    week = [date - datetime.timedelta(days=weekday-dt) for dt in xrange(weekday)]

    while day.month==date.month or weekday!=6:
        week.append(day)
        weekday = day.weekday()
        if weekday == 6:
            weeks.append(week)
            week = []
        day += datetime.timedelta(days=1)
    
    calendar.append(weeks)
    
    return calendar

def add_minutes_to_time(time, minutes):
    t_hour = time.hour
    t_minute = time.minute
    
    new_minutes = (time.minute + minutes) % 60
    new_hour = (time.hour + (time.minute + minutes) / 60) % 24
    
    return datetime.time(new_hour, new_minutes)


def minutes_difference(time1, time2):
    today = datetime.date.today()
    time1 = datetime.datetime.combine(today, time1)
    time2 = datetime.datetime.combine(today, time2)
    if time1 < time2:
        time1 + datetime.timedelta(days=1)
    return (time1 - time2).seconds / 60.0

def minutes_to_time(minutes, format='%sh %sm'):
    minutes = int(minutes)
    hour = int(minutes) / 60
    minutes = minutes % 60
    
    return format % (hour, minutes)

def convert_datetime(dt, tz_from, tz_to):
    try:
        tz_from = pytz.timezone(tz_from)
    except:
        pass

    try:
        tz_to = pytz.timezone(tz_to)
    except:
        pass
    
    return dt + (dt.replace(tzinfo=tz_from) - dt.replace(tzinfo=tz_to))

def difference_in_minutes(d1, d2):
    tdays = d1 - d2 
    min, sec = divmod(tdays.days*86400 + tdays.seconds, 60)
    return min