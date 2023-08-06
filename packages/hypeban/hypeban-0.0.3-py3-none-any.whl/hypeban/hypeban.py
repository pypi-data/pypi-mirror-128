from datetime import datetime

def contains_dashes(date):
    if "-" in date:
        return True
    else:
        print("Invalid date format")
        return False

def days_since_date(date, date_format):
    then = datetime.strptime(date, date_format)
    print("Date input:", then.strftime(date_format))
    now = datetime.now()
    days_since = (now - then).days
    return days_since

def days_until_date(date, date_format):
    then = datetime.strptime(date, date_format)
    print("Date input:", then.strftime(date_format))
    now = datetime.now()
    days_until = (then - now).days
    return days_until