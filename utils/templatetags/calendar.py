# Template tag
from datetime import date, timedelta, datetime
from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()



def get_last_day_of_month(year, month):
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)

def get_prev_month(year, month):
    if (month == 1):
        year -= 1
        month = 12
    else:
        month -= 1
    return date(year, month, 1)

def get_next_month(year, month):
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1)


def month_cal(baseurl, year=date.today().year, month=date.today().month, app_label='blog', model_name='post'):
    content_type = ContentType.objects.get(app_label=app_label, model=model_name)
    model = content_type.model_class()

    datefield = 'date'
    key_year = ('%s__year'%datefield).encode('utf8')
    key_month = ('%s__month'%datefield).encode('utf8')
    filters={key_year:year, key_month:month, 'is_draft':False, '%s__lte'%datefield:datetime.now()}
    event_list = model.objects.filter(**filters)

    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())

    month_cal = []
    week = []
    week_headers = []

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['event'] = False
        for event in event_list:
            if day >= getattr(event,datefield).date() and day <= getattr(event,datefield).date():
                cal_day['event'] = True
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False  
        week.append(cal_day)
        if day.weekday() == 6:
            month_cal.append(week)
            week = []
        i += 1
        day += timedelta(1)

    return {'calendar': month_cal, 'headers': week_headers, 
            'prev_month': get_prev_month(year, month), 
            'next_month': get_next_month(year, month),
            'baseurl':baseurl.rstrip('/'),
            'basedate':first_day_of_month}

register.inclusion_tag('blog/calendar.html')(month_cal)