import requests as rq
from datetime import datetime, timedelta
import time

MAX_ATTEMPT = 10


def timestamp_to_datestr(_timestamp, _format=None) -> str:
    """
    :param _timestamp: UNIX timestamp
    :param _format: datestr format, default as YYYY-MM-DD
    :return: datestr in specific format
    """
    if _format:
        return datetime.fromtimestamp(_timestamp).strftime(_format)
    else:
        return datetime.fromtimestamp(_timestamp).strftime('%Y-%m-%d')


def datestr_to_timestamp(_datestr) -> int:
    """
    :param _datestr: datestr in YYYY-MM-DD format
    :return: UNIX timestamp
    """
    return int(format((time.mktime(datetime.strptime(_datestr,
                                                     '%Y-%m-%d').timetuple())), '.10g'))


def datestr_to_timestamp_ddmmyy(_datestr) -> int:
    """
    :param _datestr: datestr in DD-MM-YYYY format
    :return: UNIX timestamp
    """
    return int(format((time.mktime(datetime.strptime(_datestr,
                                                     '%d-%m-%Y').timetuple())), '.10g'))


def reverse_data_str(_datestr) -> str:
    """
    :param _datestr: date string
    :return: date str in reversed format YYYY-MM-DD <-> DD-MM-YYYY
    """
    return '-'.join(_datestr.split('-')[::-1])


def compare_date(a, b):
    """
    :param a: date str a in YYYY-MM-DD format
    :param b: date str b in YYYY-MM-DD format
    :return: True if a is later than b
    """
    a = datetime.strptime(a, '%Y-%m-%d')
    b = datetime.strptime(b, '%Y-%m-%d')
    return a > b


def date_increment(_date, _days):
    """
    :param _date: date string
    :param _days: number of days to be incremented
    :return:
    """
    return datetime.strftime(_date + timedelta(days=_days), '%Y-%m-%d')


def formatted_reverse_datestr(_datestr):
    """
    :param _datestr: datestr in dd/mm/YYYY format e.g. 15-8-2022
    :return: datestr in YYYY/MM/DD format e.g. 2022-08-15
    """
    f_datestr = datetime.strptime(_datestr, "%d-%m-%Y")
    return datetime.strftime(f_datestr, '%Y-%m-%d')


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def get_list_of_month(start, end):
    arr = []
    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    while start < end:
        arr.append(last_day_of_month(start).strftime('%Y-%m-%d'))
        start += timedelta(days=31)
    return arr


def get(endpoint):
    attempt = 0
    while attempt < MAX_ATTEMPT:
        attempt += 1
        try:
            res = rq.get(endpoint)
            if res.status_code == 200:
                return res.json()
            elif res.status_code == 429:
                time.sleep(int(res.headers["Retry-After"]))
            else:
                time.sleep(2)
        except Exception as e:
            print(e)
