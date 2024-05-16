from datetime import datetime, timedelta
import os


def datetime_now():
    return datetime.now()

def check_for_numeric(value):
    return_val = value
    try:
        return_val = float(value)
    except ValueError:
        return_val = None

    return return_val


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_date_time(value):
    date_formats = ["%Y-%m-%d %H:%M:%S", "%H:%M:%S"]
    now = datetime.utcnow()
    date_time = None
    for ndx, date_format in enumerate(date_formats):
        try:
            date_time = datetime.strptime(value, date_format)
            break
        except (TypeError, ValueError):
            ndx = -1

    if ndx == 1:
        date_time = datetime.replace(date_time, year=now.year, month=now.month, day=now.day)
        if date_time < now:
            date_time = date_time + timedelta(days=1)
    elif ndx == -1:
        date_time = None
    return date_time

def deployment_time_to_format(deployment_time: datetime):
    return deployment_time.strftime("%Y-%m-%d %H:%M:%S")
