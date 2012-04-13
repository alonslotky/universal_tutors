import datetime

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
