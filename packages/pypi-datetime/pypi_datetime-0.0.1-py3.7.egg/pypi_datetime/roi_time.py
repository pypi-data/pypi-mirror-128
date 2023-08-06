import datetime
import time as _time
import pytz


def time():
    """
    返回当前时间戳
    :return:
        _time.time()：例:1634041961.0349388
    """
    return _time.time()


def now_time():
    """
    当前上海时间
    :return:
        now_time: 例:2021-10-12 20:46:28
    """
    now_time = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    # now_time = "%s-%s-%s %s:%s:%s" % (
    #     now_time.year, now_time.month, now_time.day, now_time.hour, now_time.minute, now_time.second)
    # now_time = datetime.datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    now_time = datetime.datetime(now_time.year, now_time.month, now_time.day, now_time.hour, now_time.minute,
                                 now_time.second)
    return now_time


def utc_now_time():
    """
    当前utc时间
    Returns:
        utc_time: 例:2021-10-12 12:46:28
    """
    utc_time = datetime.datetime.utcnow()
    utc_time = datetime.datetime(utc_time.year, utc_time.month, utc_time.day, utc_time.hour, utc_time.minute,
                                 utc_time.second)
    return utc_time
