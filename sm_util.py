import datetime
import time

def str2timestamp(str, format):
    dt = datetime.datetime.strptime(str, format)
    return  time.mktime(dt.timetuple())

def timestamp2date(timestamp):
    return time.strftime("%Y-%m-%d", time.localtime(timestamp))
